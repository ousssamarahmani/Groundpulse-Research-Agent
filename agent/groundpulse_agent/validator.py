from __future__ import annotations

from typing import Any

from .models import ClaimLedger


def validate_ledger(
    ledger: ClaimLedger,
    raw_source: Any,
    allowed_source_ids: set[str],
) -> list[dict[str, str]]:
    """Return validation errors; an empty list means the ledger passed."""
    errors: list[dict[str, str]] = []

    record = raw_source[0] if isinstance(raw_source, list) else raw_source
    available_fields = set(record.keys())

    for claim in ledger.claims:
        for source_id in claim.source_ids:
            if source_id not in allowed_source_ids:
                errors.append({
                    "claim_id": claim.claim_id,
                    "rule": "allowed_source",
                    "reason": f"Unknown source ID: {source_id}",
                })

        if claim.classification == "source-backed":
            if not claim.source_ids:
                errors.append({
                    "claim_id": claim.claim_id,
                    "rule": "source_required",
                    "reason": "Source-backed claim has no source ID",
                })

            if not claim.source_fields:
                errors.append({
                    "claim_id": claim.claim_id,
                    "rule": "field_required",
                    "reason": "Source-backed claim has no source field",
                })

            for field in claim.source_fields:
                if field not in available_fields:
                    errors.append({
                        "claim_id": claim.claim_id,
                        "rule": "field_exists",
                        "reason": f"Source field does not exist: {field}",
                    })

        elif claim.classification == "derived":
            if not claim.source_ids:
                errors.append({
                    "claim_id": claim.claim_id,
                    "rule": "derivation_source",
                    "reason": "Derived claim has no source ID",
                })

            if not claim.derivation_inputs:
                errors.append({
                    "claim_id": claim.claim_id,
                    "rule": "derivation_inputs",
                    "reason": "Derived claim has no derivation inputs",
                })

        elif claim.classification == "gap":
            if not claim.gap_reason:
                errors.append({
                    "claim_id": claim.claim_id,
                    "rule": "gap_reason",
                    "reason": "Gap claim has no explanation",
                })

    return errors
