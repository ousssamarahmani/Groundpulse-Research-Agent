# GroundPulse Research Agent — Ground-Truth Spec

This project republishes the existing GroundPulse Research Agent from the provided GitHub repository. The source application is the reference implementation; fidelity to its current product language takes priority over introducing a new visual direction.

## Reference Direction

The interface uses an editorial space-operations aesthetic: near-black orbital imagery, cool white typography, restrained violet emphasis, thin technical rules, evidence-package cards, and asymmetric two-column compositions. The emotional intent is rigorous, calm, and operational rather than playful or consumer-oriented.

## Design Movement

Contemporary mission-control editorialism: a hybrid of aerospace instrument panels, technical documentation, and premium research-product landing pages.

## Core Principles

1. Evidence before language: surface provenance, validation, claims, and gaps before synthesis.
2. Quiet technical confidence: use sparse layouts, precise labels, and restrained motion rather than decorative clutter.
3. Space as context: orbital imagery, low-key lighting, and fine signal lines establish the domain without overpowering the content.
4. Inspectable output: every major CTA should lead toward a visible product artifact or workflow.

## Color Philosophy

The palette is intentionally low-key so the product’s evidence states and violet signal accents carry attention. Near-black backgrounds create the feeling of deep space and a focused operations room; white and cool-gray text keep long-form explanation legible; violet is reserved for active validation, emphasis, and directional energy.

## Layout Paradigm

Use wide, asymmetric editorial sections with anchored copy on the left and visual/product evidence modules on the right. Favor horizontal rules, open negative space, and deliberate vertical pacing over uniform card grids. Dashboard-like areas use persistent navigation and dense but readable evidence rows.

## Signature Elements

- Violet signal dots, orbital traces, and validation indicators.
- Thin technical rules with small uppercase operational labels.
- Floating product previews that resemble research packets, claim ledgers, and agent-run status panels.

## Interaction Philosophy

Interactions should feel like inspecting a mission packet: direct, reversible, and explicit. Buttons should provide clear state feedback, while placeholder actions should disclose when a capability is not yet connected. Motion is subtle and functional, with no distracting loops.

## Animation

Use short ease-out transitions for buttons, navigation, tabs, and panels. Reveal grouped content with modest staggered opacity/transform motion only when it clarifies hierarchy. Respect prefers-reduced-motion and avoid animated layout properties.

## Typography System

Preserve the repository’s current typography and hierarchy. Headlines are large, high-contrast, and editorial; supporting copy is neutral and compact; metadata uses tracked uppercase labels and small technical numerals. Do not replace the existing font system unless required by the build.

## Brand Essence

GroundPulse is an evidence-first research coordinator for satellite and ground-segment teams that need an answer they can inspect, cite, and defend. Personality: rigorous, calm, operational.

## Brand Voice

Headlines should be concise, specific, and slightly editorial. CTAs should name the artifact or next inspection step rather than use generic filler.

Example lines:

- “Your space data research team—in one agent.”
- “Not chat history. Deliverables you can inspect.”

## Wordmark & Logo

Preserve the existing GroundPulse satellite-dish mark and wordmark from the source repository. The mark should remain visible in the header and as the favicon where supported.

## Signature Brand Color

Signal violet: `#9b6cff` — reserved for validation status, active navigation, orbital highlights, and important emphasis.

## Publishing Notes

The source repository is a Vite + React + TypeScript application. The managed project should preserve the existing `/`, `/dashboard`, and `/journal/claim-ledger` routes and use a static-compatible build without changing backend behavior.

## Style Decisions

- Preserve existing source visuals and content for this publishing migration.
- Do not introduce a new visual system or substitute generic placeholder imagery.
- Keep the published experience aligned with the reference application’s dark aerospace editorial language.
