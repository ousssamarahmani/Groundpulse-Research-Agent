# Demo Guide

## Purpose

This guide shows how to demonstrate the current prototype honestly during a hackathon review. The goal is to communicate the product workflow and evidence model without presenting local interface values as live operational records.

## Start the interface

```bash
pnpm install
pnpm dev
```

Open the Vite URL printed in the terminal. Use `/` for the landing page, `/dashboard` for Mission Control, and `/journal/claim-ledger` for a sample methodology note.

## Suggested live demonstration

| Step | Screen | What to show | What to say |
|---|---|---|---|
| **1** | Landing page | The four-stage workflow and package outputs. | “GroundPulse is designed to move from a structured question to a reviewable evidence package.” |
| **2** | Dashboard | Mission path, evidence filters, tabs, and visible data gap. | “This is a local interactive prototype of the controls we will connect to a durable research-run backend.” |
| **3** | New research dialog | Request framing fields and validation-rule notice. | “A production request is intended to create a run ID, capture source constraints, and enqueue background work.” |
| **4** | Journal and documentation | Claim ledger principles and implementation plan. | “The product is designed to preserve source boundaries instead of producing unsupported conclusions.” |

## Demonstration boundary

The current dashboard uses interface-only state. Do not describe a demo row, source count, package ID, timestamp, or agent trace as a live record. Do not claim a deployed GCP backend, active source ingestion, live satellite telemetry, or an empirical model result. The appropriate phrasing is **“prototype workflow”** or **“target implementation path.”**
