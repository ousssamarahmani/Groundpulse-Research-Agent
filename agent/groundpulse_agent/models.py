from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Classification = Literal["source-backed", "derived", "gap"]


class ApprovedSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    url: str
    provider: str
    source_type: str


class P0Scope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scope_id: str
    question: str
    decision_intent: str
    object: dict[str, str]
    approved_sources: list[ApprovedSource]
    allowed_claim_types: list[Classification]
    non_claims: list[str]
    prompt_version: str
    schema_version: str


class Claim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    claim: str = Field(min_length=1)
    classification: Classification
    source_ids: list[str] = Field(default_factory=list)
    source_fields: list[str] = Field(default_factory=list)
    derivation_inputs: list[str] = Field(default_factory=list)
    gap_reason: str | None = None


class ClaimLedger(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    claims: list[Claim] = Field(min_length=1)
