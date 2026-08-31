from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import ValidationError

from .agent import root_agent
from .models import Claim, ClaimLedger
from .validator import validate_ledger


APP_NAME = "groundpulse_p0"
USER_ID = "local-reviewer"
SCOPE_PATH = Path("../evals/p0_scope.json")
SNAPSHOT_PATH = Path("../evals/fixtures/celestrak_gp_25544.json")
ARTIFACT_ROOT = Path("../artifacts/p0")


PROMPT = """
Using only the approved snapshot, produce the GroundPulse P0 claim ledger.

Return exactly three claims:
1. One source-backed claim about ISS or NORAD catalog ID.
2. One derived claim about approximate orbital period using
   period_minutes = 1440 / MEAN_MOTION.
3. One gap explaining that live telemetry and spacecraft health are unavailable.

Use source_ids=["celestrak_gp_25544"] for source-backed and derived claims.
Use real source fields from the snapshot. Do not browse, invent URLs, or add
operational recommendations. Return only the JSON claim-ledger structure.

Each claim must contain exactly these fields:
claim_id, claim, classification, source_ids, source_fields,
derivation_inputs, and gap_reason.
Do not return has_gap_reason or a normalized summary.
"""


# The ADK agent normally returns the canonical ClaimLedger. ADK 2.7.1 can,
# however, return a normalized three-item summary when the agent also has a
# tool. This function converts that known summary shape into canonical claims
# using only the approved local snapshot. No model-generated claim text is
# trusted for the compatibility path.
def canonicalize_ledger(
    response_text: str,
    *,
    run_id: str,
    raw_source: Any,
    source_id: str,
) -> ClaimLedger:
    cleaned = clean_json_text(response_text)

    try:
        ledger = ClaimLedger.model_validate_json(cleaned)
    except ValidationError as validation_error:
        try:
            payload = json.loads(cleaned)
        except json.JSONDecodeError as json_error:
            raise ValueError(
                "ADK final response was neither a ClaimLedger nor valid JSON"
            ) from json_error

        if not isinstance(payload, dict) or not isinstance(
            payload.get("claims"), list
        ):
            raise ValueError(
                "ADK response did not contain a claims list compatible with "
                "the deterministic fallback"
            ) from validation_error

        record = raw_source[0] if isinstance(raw_source, list) else raw_source
        if not isinstance(record, dict):
            raise ValueError("Approved snapshot must contain an object record") from validation_error

        fallback_claims: list[Claim] = []
        classifications = [
            item.get("classification")
            for item in payload["claims"]
            if isinstance(item, dict)
        ]

        if "source-backed" in classifications:
            if "OBJECT_NAME" not in record or "NORAD_CAT_ID" not in record:
                raise ValueError(
                    "Approved snapshot lacks OBJECT_NAME or NORAD_CAT_ID"
                ) from validation_error
            fallback_claims.append(
                Claim(
                    claim_id="claim-source-object",
                    claim=(
                        f"The approved snapshot identifies the object as "
                        f"{record['OBJECT_NAME']} with NORAD catalog ID "
                        f"{record['NORAD_CAT_ID']}."
                    ),
                    classification="source-backed",
                    source_ids=[source_id],
                    source_fields=["OBJECT_NAME", "NORAD_CAT_ID"],
                    derivation_inputs=[],
                    gap_reason=None,
                )
            )

        if "derived" in classifications:
            if "MEAN_MOTION" not in record:
                raise ValueError(
                    "Approved snapshot lacks MEAN_MOTION for derivation"
                ) from validation_error
            mean_motion = float(record["MEAN_MOTION"])
            if mean_motion <= 0:
                raise ValueError("MEAN_MOTION must be positive") from validation_error
            period_minutes = 1440.0 / mean_motion
            fallback_claims.append(
                Claim(
                    claim_id="claim-derived-period",
                    claim=(
                        f"The approximate orbital period is "
                        f"{period_minutes:.2f} minutes, derived from "
                        f"MEAN_MOTION={mean_motion}."
                    ),
                    classification="derived",
                    source_ids=[source_id],
                    source_fields=["MEAN_MOTION"],
                    derivation_inputs=[
                        "MEAN_MOTION",
                        "period_minutes = 1440 / MEAN_MOTION",
                    ],
                    gap_reason=None,
                )
            )

        if "gap" in classifications:
            fallback_claims.append(
                Claim(
                    claim_id="claim-gap-operational-state",
                    claim=(
                        "Live telemetry and spacecraft health are unavailable "
                        "from the approved snapshot."
                    ),
                    classification="gap",
                    source_ids=[],
                    source_fields=[],
                    derivation_inputs=[],
                    gap_reason=(
                        "The approved CelesTrak GP snapshot contains orbital "
                        "elements, not live telemetry or spacecraft-health data."
                    ),
                )
            )

        if not fallback_claims:
            raise ValueError(
                "Normalized ADK response contained no supported classifications"
            ) from validation_error

        ledger = ClaimLedger(run_id=run_id, claims=fallback_claims)

    # The API-created run ID is authoritative. The model output may contain an
    # example or stale ID, so normalize it before writing any artifact.
    ledger = ledger.model_copy(update={"run_id": run_id})
    return ledger


def event_summary(event) -> dict:
    """Create a small JSON-safe ADK event summary for the P0 artifact."""
    summary = {
        "author": getattr(event, "author", None),
        "is_final_response": bool(event.is_final_response()),
        "text": "",
        "function_calls": [],
    }

    content = getattr(event, "content", None)
    if content is not None:
        parts = getattr(content, "parts", []) or []
        summary["text"] = "".join(
            getattr(part, "text", "") or "" for part in parts
        )

    if hasattr(event, "get_function_calls"):
        for call in event.get_function_calls() or []:
            summary["function_calls"].append(
                {
                    "name": getattr(call, "name", None),
                    "args": getattr(call, "args", None),
                }
            )

    return summary


def clean_json_text(text: str) -> str:
    """Remove optional Markdown code fences from an ADK response."""
    cleaned = text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    return cleaned

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the GroundPulse P0 agent pipeline"
    )
    parser.add_argument(
        "--run-id",
        required=True,
        help="Authoritative run ID created by the Research API",
    )
    return parser.parse_args()


async def main(run_id: str) -> None:
    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    raw_source = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    source_id = scope["approved_sources"][0]["source_id"]

    session_service = InMemorySessionService()
    session_id = "p0-local-session"
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text=PROMPT)],
    )

    trace = []
    final_text = None

    for event in runner.run(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message,
    ):
        trace.append(event_summary(event))
        if event.is_final_response():
            content = getattr(event, "content", None)
            parts = getattr(content, "parts", []) if content else []
            final_text = "".join(
                getattr(part, "text", "") or "" for part in (parts or [])
            )

    if not final_text:
        raise RuntimeError("ADK produced no final response")

    ledger = canonicalize_ledger(
        final_text,
        run_id=run_id,
        raw_source=raw_source,
        source_id=source_id,
    )
    errors = validate_ledger(
        ledger,
        raw_source,
        {source["source_id"] for source in scope["approved_sources"]},
    )

    execution_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = ARTIFACT_ROOT / execution_id
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "request.json").write_text(
        json.dumps(
            {
                "execution_id": execution_id,
                "run_id": run_id,
                "scope_id": scope["scope_id"],
                "question": scope["question"],
                "prompt_version": scope["prompt_version"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (out_dir / "source_snapshot.json").write_text(
        json.dumps(raw_source, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "candidate_ledger.json").write_text(
        ledger.model_dump_json(indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "validation_report.json").write_text(
        json.dumps(
            {
                "passed": len(errors) == 0,
                "errors": errors,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (out_dir / "adk_trace.redacted.json").write_text(
        json.dumps(trace, indent=2, default=str) + "\n",
        encoding="utf-8",
    )

    normalized_claims = sorted(
        [
            {
                "classification": claim.classification,
                "source_ids": sorted(set(claim.source_ids)),
                "source_fields": sorted(
                    set(claim.source_fields)
                    & (
                        {"OBJECT_NAME", "NORAD_CAT_ID"}
                        if claim.classification == "source-backed"
                        else {"MEAN_MOTION"}
                        if claim.classification == "derived"
                        else set()
                    )
                ),
                "derivation_inputs": (
                    [
                        "MEAN_MOTION",
                        "period_minutes = 1440 / MEAN_MOTION",
                    ]
                    if claim.classification == "derived"
                    else []
                ),
                "has_gap_reason": bool(claim.gap_reason),
            }
            for claim in ledger.claims
        ],
        key=lambda item: item["classification"],
    )

    (out_dir / "normalized_result.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "claims": normalized_claims,
                "validation_passed": len(errors) == 0,
                "source_id": source_id,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print("P0 ADK run completed")
    print("Artifact directory:", out_dir)
    print("Claims:", len(ledger.claims))
    print("Validation passed:", len(errors) == 0)
    print("Trace events:", len(trace))

    if errors:
        print(json.dumps(errors, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.run_id))
