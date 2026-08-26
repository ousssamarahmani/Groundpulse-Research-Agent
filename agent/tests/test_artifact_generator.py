from __future__ import annotations

import json
from pathlib import Path

from groundpulse_agent.artifact_generator import generate_research_package


def test_generate_research_package_is_deterministic(tmp_path: Path) -> None:
    artifact_directory = tmp_path / "artifact"
    artifact_directory.mkdir()
    normalized = {
        "run_id": "run_p1_test001",
        "claims": [
            {
                "claim_id": "claim_001",
                "claim": "The object is ISS (ZARYA).",
                "classification": "source-backed",
                "source_ids": ["celestrak_gp_25544"],
                "source_fields": ["OBJECT_NAME"],
                "derivation_inputs": [],
                "gap_reason": None,
            },
            {
                "claim_id": "claim_002",
                "claim": "Live telemetry is unavailable.",
                "classification": "gap",
                "source_ids": [],
                "source_fields": [],
                "derivation_inputs": [],
                "gap_reason": "The approved snapshot contains no live telemetry.",
            },
        ]
    }
    (artifact_directory / "normalized_result.json").write_text(
        json.dumps(normalized),
        encoding="utf-8",
    )

    generate_research_package(
        artifact_directory=artifact_directory,
        run_id="run_p1_test001",
        source_id="celestrak_gp_25544",
        validation_passed=True,
    )
    first_gap = (artifact_directory / "gap_list.json").read_text(encoding="utf-8")
    first_brief = (artifact_directory / "brief.md").read_text(encoding="utf-8")
    first_manifest = (artifact_directory / "package_manifest.json").read_text(
        encoding="utf-8"
    )

    generate_research_package(
        artifact_directory=artifact_directory,
        run_id="run_p1_test001",
        source_id="celestrak_gp_25544",
        validation_passed=True,
    )

    assert (artifact_directory / "gap_list.json").read_text(encoding="utf-8") == first_gap
    assert (artifact_directory / "brief.md").read_text(encoding="utf-8") == first_brief
    assert (
        (artifact_directory / "package_manifest.json").read_text(encoding="utf-8")
        == first_manifest
    )


def test_gap_list_contains_only_gap_claims(tmp_path: Path) -> None:
    artifact_directory = tmp_path / "artifact"
    artifact_directory.mkdir()
    (artifact_directory / "normalized_result.json").write_text(
        json.dumps(
            {
                "run_id": "run_p1_test002",
                "claims": [
                    {
                        "claim_id": "claim_001",
                        "claim": "A fact.",
                        "classification": "source-backed",
                        "source_ids": ["source"],
                        "source_fields": ["FIELD"],
                        "derivation_inputs": [],
                        "gap_reason": None,
                    },
                    {
                        "claim_id": "claim_002",
                        "claim": "A missing metric.",
                        "classification": "gap",
                        "source_ids": [],
                        "source_fields": [],
                        "derivation_inputs": [],
                        "gap_reason": "Metric absent from source.",
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    generate_research_package(
        artifact_directory=artifact_directory,
        run_id="run_p1_test002",
        source_id="source",
        validation_passed=True,
    )

    payload = json.loads(
        (artifact_directory / "gap_list.json").read_text(encoding="utf-8")
    )
    assert payload["schema_version"] == "research-gap-list.v1"
    assert len(payload["gaps"]) == 1
    assert payload["gaps"][0]["claim_id"] == "claim_002"


def test_package_manifest_lists_generated_files(tmp_path: Path) -> None:
    artifact_directory = tmp_path / "artifact"
    artifact_directory.mkdir()
    (artifact_directory / "normalized_result.json").write_text(
        json.dumps(
            {
                "run_id": "run_p1_test003",
                "claims": [
                    {
                        "claim_id": "claim_001",
                        "claim": "A fact.",
                        "classification": "source-backed",
                        "source_ids": ["source"],
                        "source_fields": ["FIELD"],
                        "derivation_inputs": [],
                        "gap_reason": None,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    generate_research_package(
        artifact_directory=artifact_directory,
        run_id="run_p1_test003",
        source_id="source",
        validation_passed=True,
    )

    payload = json.loads(
        (artifact_directory / "package_manifest.json").read_text(encoding="utf-8")
    )
    assert payload["schema_version"] == "research-package.v1"
    assert payload["gap_count"] == 0
    assert "gap_list.json" in payload["artifact_files"]
    assert "brief.md" in payload["artifact_files"]
