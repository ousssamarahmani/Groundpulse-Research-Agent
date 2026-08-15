# Security Policy

## Supported scope

The current repository is a prototype frontend and documentation package. It does not ship a production API, persistent datastore, cloud credentials, or telemetry ingestion endpoint.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability, exposed credential, private source record, or sensitive station-log disclosure. Contact the repository maintainer privately through the GitHub security advisory workflow once the repository is created, and include a concise reproduction path and impact description.

## Security requirements for future services

Production work must use least-privilege service identities, server-side secret storage, authenticated service-to-service requests, immutable artifact manifests, audit logging, and explicit source authorization. No API credential or telemetry payload belongs in the browser bundle, test fixture, screenshot, or issue thread.
