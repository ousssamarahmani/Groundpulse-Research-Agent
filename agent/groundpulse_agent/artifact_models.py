from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class GapItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_id: str
    claim: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class GapList(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = "research-gap-list.v1"
    run_id: str
    gaps: list[GapItem]


class PackageManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = "research-package.v1"
    run_id: str
    source_id: str
    validation_passed: bool
    artifact_files: list[str]
    gap_count: int
