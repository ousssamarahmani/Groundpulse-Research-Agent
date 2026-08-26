from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .models import ClaimLedger


load_dotenv()


PROMPT = """
You are the GroundPulse P0 evidence coordinator.

Use only the approved CelesTrak snapshot included below.
Return only JSON matching the requested claim-ledger structure.

Create exactly three claims:
1. One source-backed claim about the object name or catalog ID.
2. One derived claim about approximate orbital period using:
   period_minutes = 1440 / MEAN_MOTION
   Include MEAN_MOTION in derivation_inputs.
3. One gap explaining that live telemetry and spacecraft health are unavailable.

Allowed classifications are exactly: source-backed, derived, gap.
Do not invent facts, URLs, sources, telemetry, spacecraft health, or operational recommendations.
Every source-backed and derived claim must use source_ids=["celestrak_gp_25544"].

Approved source snapshot:
"""


# Use the Gemini API's supported schema representation instead of passing
# Pydantic's generated JSON schema directly.
GEMINI_CLAIM_LEDGER_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "run_id": types.Schema(type=types.Type.STRING),
        "claims": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "claim_id": types.Schema(type=types.Type.STRING),
                    "claim": types.Schema(type=types.Type.STRING),
                    "classification": types.Schema(type=types.Type.STRING),
                    "source_ids": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                    ),
                    "source_fields": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                    ),
                    "derivation_inputs": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                    ),
                    "gap_reason": types.Schema(type=types.Type.STRING),
                },
                required=["claim_id", "claim", "classification"],
            ),
        ),
    },
    required=["run_id", "claims"],
)


def main() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "PASTE_YOUR_GEMINI_KEY_HERE":
        raise RuntimeError("GOOGLE_API_KEY is missing from agent/.env")

    snapshot_path = Path("../evals/fixtures/celestrak_gp_25544.json")
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    prompt = PROMPT + json.dumps(snapshot, indent=2)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-flash-latest"),
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GEMINI_CLAIM_LEDGER_SCHEMA,
            temperature=0,
        ),
    )

    # Pydantic remains the application-level authority after Gemini returns.
    ledger = ClaimLedger.model_validate_json(response.text)
    print("Gemini smoke test passed")
    print("Run ID:", ledger.run_id)
    print("Claims returned:", len(ledger.claims))
    for claim in ledger.claims:
        print(f"- {claim.classification}: {claim.claim}")


if __name__ == "__main__":
    main()
