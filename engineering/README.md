# Engineer handoff: execution order

The [agent-team brief](./AGENT-TEAM-BRIEF.md) is a copy-ready prompt for the engineer's orchestrator. Give the team these three files first: [master build specification](../Technical-Build-Spec.md), [core media/ML specification](../Core-Media-and-ML-Engineering-Spec.md), and [accuracy rule](../Listing-Accuracy-Standard.md). The master spec's WP-00 through WP-12 table is the task breakdown. WP-00 inspects the *existing* Crankshaft website, verifier, routing and CRM code before assigning parallel implementation. The supplied contracts are proposed canonical interfaces; the lead engineer maps them to the real stack and versions any change.

## Required first PR

1. `integration-map.md`: actual repositories, existing auth/tenant model, verifier event shape, CRM handoff, inventory lookup, hosting/queue/object-store choices and dealer vendor permissions.
2. An architecture decision record for what will be reused and how Python media/ML workers communicate with the existing application.
3. Updated, validated OpenAPI/event schemas derived from [the starter API](./contracts/listing-api.openapi.yaml) and [event schema](./contracts/event-envelope.schema.json), with generated types in the actual stack.
4. A synthetic fixture for one dealer, two stock lifecycles, one 90-second phone video, two call outcomes and one confirmed appointment. No real caller PII or unauthorized marketplace media.
5. CI jobs for schema checks, unit/integration tests and a static HTML/package link check.

Work packages can then proceed in parallel. Every PR states which acceptance row it satisfies, what fixture proves it, what remains mocked, how to roll it back, and whether it changes the existing live call path. A model-training PR must include its data-rights manifest and dealer/time holdout report; an inference PR cannot be merged on training accuracy alone.
