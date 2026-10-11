# Paste into the engineering team's orchestrator

Build Crankshaft's Listing Tuner as a service integrated with the **existing** Crankshaft website, AI verifier, SignalWire call routing and any existing CRM handoff. Do not rebuild those systems. Start by reading [Technical Build Specification](../Technical-Build-Spec.md), [Core Media and ML Engineering Specification](../Core-Media-and-ML-Engineering-Spec.md), [Listing Accuracy Standard](../Listing-Accuracy-Standard.md), and the proposed [API contract](./contracts/listing-api.openapi.yaml). Inspect the real existing repositories before coding; this public package does not include their source, credentials or verified APIs.

## First assignment: lead/integration agent

Produce `integration-map.md` and an architecture decision record. Identify existing language/framework, identity/tenant model, verifier event/stock lookup/CRM interfaces, hosting, database, queue and storage. Replace proposed contract names with actual mappings and publish one shared OpenAPI/event schema version. Create synthetic fixtures for two cars, a dealer feed, a phone walkaround, call outcomes and an appointment. Do not allow parallel agents to invent incompatible schemas. Flag vendor access that requires dealer authorization; mock it until access exists.

## Parallel assignments after contracts merge

1. **Inventory/facts agent:** stock lifecycle, DMS adapter, vPIC identity cache, dealer attestation/conflict API, sold/price change logic. Return current source revision and fact provenance.
2. **Capture/frontend agent:** existing-auth mobile upload flow, stock selection, photo/video prompts, resumable direct upload, operator/dealer review screens. Preserve the existing public site and login experience.
3. **Photo agent:** immutable originals, image QA/view classification, reproducible real-photo edit recipes and gallery selection. Sharpen as useful; do not remove dents, change car color/parts/condition or use synthetic vehicle imagery.
4. **Video agent:** probe, transcript/scene map, candidate intervals, optional Jev ranker behind a flag, edit decision list, FFmpeg renders, complete clip review and retake path.
5. **Copy/QA agent:** structured dealer-sourced claim generation, direct conflict/price/disclosure validation and channel variants. No generic VIN option promoted to installed without dealer attestation.
6. **Publishing agent:** one dealer-authorized inventory/syndication write path, idempotent upsert/remove, receipt, live readback and sold withdrawal. Keep marketplace adapters behind vendor-specific authorization.
7. **Verifier/outcomes agent:** a nonblocking event bridge from the existing verifier, stock/lead attribution with confidence, CRM/DMS appointment and confirmed-sale ingest, listing-day exposure facts. Do not copy raw audio into the ML warehouse by default.
8. **ML agent:** begin with rules and the untrained photo-ranker starter, train only on authorized labeled media, hold out whole dealers/vehicles/future time, and report against a simple baseline. Build an exposure-aware qualified-appointment model only after trusted joins and denominators exist. Keep recommendations advisory until a prospective dealer test shows improvement.
9. **Platform agent:** tenant isolation, object rights/retention, queues/dead letters, contract CI, monitoring, feature flags, rollback, runbooks and fixture-driven end-to-end tests.

Use the master specification's **WP-00 to WP-12** as ticket IDs and dependencies. Each PR must name its ticket, contract version, fixture, acceptance evidence, rollback, vendor mocks and effect on the existing live call path. Merge a vertical slice (upload → draft → dealer approval → authorized publish → live check → verifier event → dealer outcome) before adding more vendors or a larger model. A failed listing job must surface a specific operator task; it must never interrupt a live call. Do not claim a trained model or conversion lift from the 40 example listings.
