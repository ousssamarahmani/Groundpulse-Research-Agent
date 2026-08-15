# GroundPulse Research Agent — Hackathon Submission

## One-line summary

GroundPulse is an evidence-first research-agent prototype that turns a structured satellite or ground-segment question into a reviewable research package rather than an unsupported AI answer.

## Problem

Space-data research often begins across incompatible public catalogs, observation networks, environmental products, internal notes, and engineering assumptions. Teams must determine whether a source fits the question, whether its timestamps and metadata align, and whether a conclusion can be defended. This work is repetitive, difficult to audit, and easy to overstate when research is compressed into a chat-like answer.

## Solution

GroundPulse models research as a controlled workflow: **frame the request → discover sources → validate evidence → build a package**. The target package contains a human-readable research brief, a claim ledger, source snapshots or links, a reproducibility manifest, and a visible list of data gaps. The interface makes validation state and uncertainty part of the product rather than hiding them behind a summary.

## Current prototype

The repository contains a static, interactive product interface with a landing page, Mission Control dashboard, Research Journal, and documentation. The dashboard demonstrates the intended controls—mission stages, source review, evidence states, gaps, package status, and new-research intake—using local presentation state. It is not connected to a live agent, cloud deployment, or real telemetry feed.

## Intended users and use case

The intended users are satellite operators, ground-station teams, research teams, and technical strategy teams. A representative use case begins with an object, location, time window, and research intent. GroundPulse collects only approved context, evaluates source fitness, and returns an evidence package for specialist review. The product is designed to reduce research operations effort; it does not replace engineering analysis or operational authority.

## Technical direction

The target service design uses a request API, durable job state, asynchronous agent work, source adapters, evidence validation, and immutable research artifacts. The planned GCP architecture separates agent orchestration from the analytics stream and uses source freshness to distinguish public near-real-time context from actual customer or partner telemetry. See [Architecture](ARCHITECTURE.md) and the [GCP integration plan](GCP_REALTIME_INTEGRATION_PLAN.md).

## Demo path

1. Open the product landing page and inspect the stated workflow and output boundaries.
2. Open `/dashboard` and select evidence filters, research tabs, and the new-research flow.
3. Open the Journal to review the claim-ledger and evidence-gate concepts.
4. Read the limitations before interpreting any displayed UI content as a production capability.

## What is deliberately not claimed

GroundPulse does not claim live satellite telemetry, operational ground-station capability, an active GCP deployment, empirical accuracy, or a released dataset. The project labels visual dashboard values as prototype content and requires a source contract, evidence gate, and human review before any production claim.
