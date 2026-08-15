# Limitations and Non-Claims

## Current repository state

This repository provides a product-interface prototype and an implementation plan. It does not provide a production Research Agent, a deployed cloud backend, a live source integration, or a reviewed empirical dataset. The landing page and dashboard must therefore be understood as interface and workflow demonstrations.

## Data boundaries

Public orbital context, public observations, and public space-weather products are distinct source classes. They must not be transformed into claimed values for SNR, Eb/N0, modem temperature, packet loss, pass success, payload health, equipment incidents, anomaly labels, or operational readiness unless an authorized source contains those measurements or a documented derivation supports them.

## Decision boundaries

GroundPulse is intended to reduce research-operations work. It does not replace engineering review, operations authorization, spacecraft safety processes, RF analysis, orbital-dynamics validation, licensing review, or a specialist’s final decision. No report should be positioned as flight, safety, or operational clearance.

## Real-time boundary

The phrase `real-time` is reserved for an authorized, documented event feed with known source timestamps and ingestion behavior. Public sources with independent publication cadence must be labeled `near-real-time` or `historical` as appropriate. Freshness must be shown to the user rather than inferred from a successful request.

## Prototype interface boundary

Any sample run IDs, mission names, state labels, evidence counts, or data-gap rows rendered by the current dashboard are local presentation content. They are not live records, customer data, source-backed research results, or evidence of a GCP deployment.
