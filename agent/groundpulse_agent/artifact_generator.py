from __future__ import annotations

import json
from pathlib import Path

from .artifact_models import GapItem, GapList, PackageManifest
from .models import ClaimLedger


def generate_research_package(
    *,
    artifact_directory: Path,
    run_id: str,
    source_id: str,
    validation_passed: bool,
) -> list[Path]:
    """Generate deterministic review artifacts from a canonical ledger file.

    Production runs provide ``candidate_ledger.json``. Older fixtures and
    callers provide the same canonical ClaimLedger envelope as
    ``normalized_result.json``. Support both inputs while never validating the
    reduced normalized summary emitted by the P0 pipeline.
    """
    candidate_path = artifact_directory / "candidate_ledger.json"
    normalized_path = artifact_directory / "normalized_result.json"

    if candidate_path.exists():
        ledger_path = candidate_path
    elif normalized_path.exists():
        ledger_path = normalized_path
    else:
        raise FileNotFoundError(
            f"Missing candidate ledger or normalized result in {artifact_directory}"
        )

    ledger = ClaimLedger.model_validate_json(
        ledger_path.read_text(encoding="utf-8")
    )

    if ledger.run_id != run_id:
        raise ValueError(
            f"Ledger run_id {ledger.run_id!r} does not match {run_id!r}"
        )

    gaps = GapList(
        run_id=run_id,
        gaps=[
            GapItem(
                claim_id=claim.claim_id,
                claim=claim.claim,
                reason=claim.gap_reason or "No gap reason supplied",
            )
            for claim in ledger.claims
            if claim.classification == "gap"
        ],
    )
    gap_path = artifact_directory / "gap_list.json"
    _write_json(gap_path, gaps.model_dump(mode="json"))

    brief_path = artifact_directory / "brief.md"
    brief_path.write_text(
        _render_brief(
            ledger=ledger,
            run_id=run_id,
            source_id=source_id,
            validation_passed=validation_passed,
        ),
        encoding="utf-8",
    )

    artifact_files = sorted(
        path.name
        for path in artifact_directory.iterdir()
        if path.is_file()
        and path.name not in {"package_manifest.json"}
    )
    package_manifest = PackageManifest(
        run_id=run_id,
        source_id=source_id,
        validation_passed=validation_passed,
        artifact_files=artifact_files,
        gap_count=len(gaps.gaps),
    )
    manifest_path = artifact_directory / "package_manifest.json"
    _write_json(manifest_path, package_manifest.model_dump(mode="json"))

    return [gap_path, brief_path, manifest_path]


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _render_brief(
    *,
    ledger: ClaimLedger,
    run_id: str,
    source_id: str,
    validation_passed: bool,
) -> str:
    lines = [
        "# GroundPulse Research Brief",
        "",
        f"- **Run ID:** `{run_id}`",
        f"- **Approved source:** `{source_id}`",
        f"- **Validation:** `{'passed' if validation_passed else 'failed'}`",
        "",
        "## Executive summary",
        "",
        (
            "This package separates source-backed facts, deterministic derivations, "
            "and evidence gaps. It does not provide live telemetry, spacecraft-health "
            "assessment, or an operational recommendation."
        ),
        "",
        "## Claims",
        "",
    ]

    for claim in ledger.claims:
        lines.extend(
            [
                f"### {claim.claim_id} — {claim.classification}",
                "",
                claim.claim,
                "",
            ]
        )
        if claim.source_ids:
            lines.append(f"**Sources:** {', '.join(claim.source_ids)}")
            lines.append("")
        if claim.source_fields:
            lines.append(f"**Source fields:** {', '.join(claim.source_fields)}")
            lines.append("")
        if claim.derivation_inputs:
            lines.append(
                f"**Derivation inputs:** {', '.join(claim.derivation_inputs)}"
            )
            lines.append("")
        if claim.gap_reason:
            lines.append(f"**Gap reason:** {claim.gap_reason}")
            lines.append("")

    lines.extend(
        [
            "## Review notes",
            "",
            (
                "Reviewers should consult `gap_list.json` for unavailable evidence "
                "and `package_manifest.json` for the deterministic package inventory."
            ),
            "",
        ]
    )
    return "\n".join(lines)
