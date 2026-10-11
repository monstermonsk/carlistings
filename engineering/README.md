# Engineer handoff: execution order

The [agent-team brief](./AGENT-TEAM-BRIEF.md) is a copy-ready prompt for the engineer's orchestrator. Give the team [master build specification](../Technical-Build-Spec.md), [connector catalog and dealer portal contract](../Connector-Catalog-and-Dealer-Portal-Spec.md), [core media/ML specification](../Core-Media-and-ML-Engineering-Spec.md), and [accuracy rule](../Listing-Accuracy-Standard.md). The master spec's WP-00 through WP-14 table is the task breakdown. WP-00 inspects only the *existing Crankshaft* website, verifier and routing code. Dealer integrations use standardized vendor adapters and self-service authorization; no per-dealer system inspection is required. The supplied contracts are proposed canonical interfaces; the lead engineer maps them to the real stack and versions any change.

## Required first PR

1. `integration-map.md`: actual Crankshaft repositories, existing auth/tenant model, verifier and SignalWire transfer event shape, CRM handoff if present, inventory lookup, hosting/queue/object-store choices. Separate vendor capability manifests document dealer/partner permissions.
2. An architecture decision record for what will be reused and how Python media/ML workers communicate with the existing application.
3. Updated, validated OpenAPI/event schemas derived from [the starter API](./contracts/listing-api.openapi.yaml) and [event schema](./contracts/event-envelope.schema.json), with generated types in the actual stack.
4. A synthetic fixture for one dealer, two staff members, two stock lifecycles, one 90-second phone video, a call with two transfer attempts and one answer, one missed/fallback call, one confirmed appointment, and CSV export. No real caller PII or unauthorized marketplace media.
5. CI jobs for schema checks, unit/integration tests and a static HTML/package link check.

Work packages can then proceed in parallel. Every PR states which acceptance row it satisfies, what fixture proves it, what remains mocked, how to roll it back, and whether it changes the existing live call path. A model-training PR must include its data-rights manifest and dealer/time holdout report; an inference PR cannot be merged on training accuracy alone.
