# Contributing to GroundPulse Research Agent

Thank you for contributing. GroundPulse accepts contributions to the interface, documentation, source controls, validation, reproducibility, and test infrastructure when they preserve the evidence-first model.

## Contribution standard

Every change must state whether it affects product interface, source ingestion, evidence validation, analytics, artifacts, or documentation. Changes that introduce a new source adapter must include a provider reference, terms or attribution review, a rate policy, stable fixture data, expected schema, and an explicit statement of what the source cannot establish.

## Pull requests

Use a focused branch and describe the problem, implementation, tests, risks, and any changed non-claims. Do not commit secrets, customer data, private station logs, unreviewed telemetry, or material that cannot be redistributed. A UI change must not imply a production service or data feed that is not present.

## Evidence rules

Source-backed claims require an accepted source record. Derived claims require recorded inputs and a reproducible method. Proposed work must be visibly labeled as proposed. Missing data must remain unavailable rather than being silently synthesized.

## Reporting issues

Use the task IDs in [docs/TASKS.md](docs/TASKS.md) where applicable. Security-sensitive reports belong in [SECURITY.md](SECURITY.md), not in public issues.
