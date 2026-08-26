from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .agent import root_agent
from .models import ClaimLedger
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
"""


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
        lines = cleaned.splitlines()
        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    return cleaned

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the GroundPulse P0 agent pipeline")
    parser.add_argument(
        "--run-id",
        required=True,
        help="Authoritative run ID created by the Research API",
    )
    return parser.parse_args()


async def main(run_id: str) -> None:
    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    raw_source = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))

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

    cleaned_final_text = clean_json_text(final_text)
    ledger = ClaimLedger.model_validate_json(cleaned_final_text)
    # The API-created run ID is authoritative. The model output may contain
    # an example or stale ID, so normalize it before writing any artifact.
    ledger = ledger.model_copy(update={"run_id": run_id})
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
                "source_id": scope["approved_sources"][0]["source_id"],
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
