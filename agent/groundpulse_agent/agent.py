from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent


load_dotenv()

SNAPSHOT_PATH = Path("../evals/fixtures/celestrak_gp_25544.json")


def read_approved_snapshot() -> dict:
    """Read the one approved CelesTrak snapshot for the GroundPulse P0 run."""
    if not SNAPSHOT_PATH.exists():
        raise FileNotFoundError(f"Approved snapshot not found: {SNAPSHOT_PATH}")

    return json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))


root_agent = Agent(
    model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite"),
    name="groundpulse_research_coordinator",
    description="Creates a source-linked candidate claim ledger from one approved snapshot.",
    instruction="""
You are the GroundPulse P0 research coordinator.

You have exactly one approved source: celestrak_gp_25544.
You have exactly one tool: read_approved_snapshot.
Call that tool before making any claims.

Use only the returned CelesTrak snapshot. Do not browse, invent URLs,
use outside knowledge, or infer live telemetry.

Return only one JSON object. Do not return Markdown, commentary, a normalized
summary, or any field named has_gap_reason.

The JSON object must have exactly these top-level fields:
{
  "run_id": "run_celestrak_gp_25544_001",
  "claims": []
}

Each claim must have exactly these fields:
claim_id, claim, classification, source_ids, source_fields,
derivation_inputs, and gap_reason.

Return exactly three claims:
1. A source-backed claim about the object name or NORAD catalog ID.
2. A derived claim about approximate orbital period using
   period_minutes = 1440 / MEAN_MOTION.
3. A gap explaining that live telemetry and spacecraft health are unavailable.

Every source-backed claim must include source_ids=["celestrak_gp_25544"]
and real source_fields from the snapshot.
Every derived claim must include source_ids=["celestrak_gp_25544"],
source_fields=["MEAN_MOTION"], and derivation_inputs including
"MEAN_MOTION" and "period_minutes = 1440 / MEAN_MOTION".
The gap claim must include a non-empty gap_reason.

The application validator, not the model, decides whether the ledger is admissible.
""",
    tools=[read_approved_snapshot],
)
