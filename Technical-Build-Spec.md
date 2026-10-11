# Crankshaft Listing Tuner: implementation specification

**Engineering handoff · Version 2 · 11 October 2026.** This is the build contract for the developer's full-stack/agentic team. **The Crankshaft website, AI call verifier and call routing already exist.** Treat those as existing services to inspect and integrate. Do not rebuild the website, voice agent, SignalWire routing or its current CRM handoff. Listing Tuner is a service within Crankshaft. The new system starts when dealer inventory and salesperson media arrive, ends when approved listings are live and reconciled, and learns from verifier and dealer outcomes. This document and the deeper [Core Media and ML Engineering Specification](./Core-Media-and-ML-Engineering-Spec.md) are the source for implementation tasks.

## 0. Build objective and non-negotiable contracts

**User story:** A dealer salesperson selects a stock unit, takes 20–30 photos and one or two phone walkarounds, and taps upload. Crankshaft matches the media to inventory, researches VIN/market context, edits *real* photos and clips, writes sourced copy, obtains dealer approval, pushes through the dealer's existing inventory publishing path, checks the live result, and reports qualified calls/appointments/sales attributable to the listing. The salesperson does not write copy or edit media.

**Existing-system boundary:** leave the production call-answering/routing path alone unless a separately reviewed adapter hook is needed to emit structured events or perform a read-only availability lookup. A failure in listing/ML infrastructure must not delay or stop a live call. The existing website is the host for a Listing Tuner service page and internal capture/review routes if its architecture permits; use a separate app behind the same identity/brand if that is safer. No duplicate login, billing entity or dealer phone system.

**Owner policy:** Dealer attestations are sufficient for condition/options. Dealer management determines online listing disclosures and approves publication. We highlight positives, do not knowingly publish false claims, and do not digitally remove dents, change paint color, parts or condition, or use an AI-created depiction as a vehicle photo. Real-photo sharpening is unrestricted by a fixed strength setting. See [Listing Accuracy Standard](./Listing-Accuracy-Standard.md). All plan minutes and token costs belong to the already-existing verifier product and billing; Listing Tuner does not introduce per-token or per-minute invoices.

**Release scope:** Cars first. One pilot dealer, one inventory source, one existing syndication/write route, one CRM/outcome source, one live channel, with additional adapters only after end-to-end acceptance. Trucks/RVs/trailers/boats/powersports use later category adapters and are not silently fed to a car-trained model.

## 1. What the team must discover before code changes

The lead engineer opens the existing Crankshaft repository(s) and produces `integration-map.md` with the actual answers below. This is a deliverable, not a reason to redesign what already works.

| Existing contract to inspect | Evidence to capture |
|---|---|
| Website/auth | Framework, identity provider, roles/tenants, deploy process, route conventions, object upload capability. |
| Verifier/call routing | Current `call_id`, dealer ID, stock lookup, qualification fields, outcome event or webhook, transfer answered status, consent/retention, failure behavior. |
| CRM path | Whether lead/appointment IDs and disposition receipts already exist; which events can be emitted without duplicate writes. |
| Inventory lookup used by verifier | Source, freshness, read API, cache TTL, sold handling and whether Listing Tuner can share the canonical stock snapshot. |
| Dealer system and syndicator | Exact vendor/version, dealer-authorized read/write method, field limits, media upload mechanics, acknowledgements, propagation delay and live verification. |
| Infrastructure | Existing database, queue, object store, secret manager, logs/traces, CI and deployment environments. Reuse compatible components. |

If an existing event is unavailable, implement the smallest adapter/emitter at its current boundary. Do not infer that the verifier exposes a field or that a DMS has a write API. The first pull request should document discovered contracts, test fixtures and any deviation from the reference architecture below.

## 2. Reference architecture and ownership

```text
Existing Crankshaft website/auth ──► dealer capture + approval UI
Existing verifier/router ──────────► signed call-event adapter ─┐
Dealer inventory/DMS ──────────────► inventory adapter ──────────┼─► Postgres event/stock/listing state
Dealer CRM/sales ──────────────────► outcome adapter ────────────┤             │
Dealer media upload ───────────────► immutable object store ──────┘             │
                                                                              outbox/queue
                                           ┌──────────────────────────────────────┼────────────────────────────┐
                                           ▼                                      ▼                            ▼
                                  Python media workers                   copy/fact worker              partner-data worker
                                           └─────────────► candidates/QA ◄────────┘                            │
                                                                 │                                           training warehouse
                                             dealer approval ► publisher adapter ► live readback                  │
                                                                 │                                           PyTorch train/eval
                                                                 └────────► listing-day/outcome joins ◄─────────┘
```

The reference deployment uses the existing application stack for APIs/UI, PostgreSQL for transactional state/outbox, S3-compatible object storage for immutable media, a durable queue for jobs and Python workers for FFmpeg/image processing/PyTorch. If existing infrastructure uses equivalent services, retain it and preserve the contracts. Keep training jobs off request/call paths. Services communicate through versioned HTTP/events and object IDs; do not pass large media through the message bus.

**Module boundaries:** `capture-api`, `inventory-adapter`, `vehicle-facts`, `photo-worker`, `video-worker`, `copy-worker`, `review-ui`, `publisher-adapter`, `verifier-event-adapter`, `outcome-adapter`, `analytics/feature-builder`, `ml-train`, `ml-infer`. Each has a named owner, schema, tests, metrics and runbook. The [Core Media and ML Engineering Specification](./Core-Media-and-ML-Engineering-Spec.md) defines internal records and algorithms; this document defines how to ship them together.

## 3. Canonical data and source authority

Use `tenant_id + stock_id + stock_lifecycle_id` as the operational key. VIN is an identity attribute, not the lifecycle key. PostgreSQL stores `dealer`, `stock_snapshot`, `fact_attestation`, `media_original`, `media_derivative`, `listing_version`, `destination_publication`, `call_event`, `lead_journey`, `outcome_event`, `job`, `approval` and `audit_event`. Append source versions and event receipts. An update never mutates the original upload or an approved historical listing version.

| Field or decision | Authority | Conflict action |
|---|---|---|
| Stock/price/mileage/availability/sold | Dealer-authorized DMS/inventory feed | Hold new publish, show discrepancy, re-read before publish and on relevant calls. |
| Actual car identity | Stock/VIN and salesperson match; free vPIC as cross-check | Quarantine mixed-car media and ask dealer. |
| Installed options/condition/history | Dealer attestation or authorized feed; optional OEM build data | Ask dealer on an obvious direct conflict; generic VIN decoder never silently adds installed features. |
| Listing disclosures/offer terms | Dealer management's destination-specific payload | Do not omit dealer-directed disclosure because a destination lacks a field; escalate mapping. |
| Buyer interest/qualification | Existing verifier's structured event | Log source/model/policy version and confidence; human corrections can supersede label for learning. |
| Appointment/retail sale | Dealer CRM/DMS confirmed disposition | Distinguish no-show, wholesale, transfer, unknown removal and retail sale. |

Free [NHTSA vPIC](https://vpic.nhtsa.dot.gov/api/) is the baseline VIN identity adapter, with cache, timeout and rate handling. Dealer-owned VIN decoder/OEM accounts and paid build-data providers are optional adapters where authorized. Normalize provider output to `candidate_fact {value, scope, provider, observed_at, cost, evidence_type}`. `scope=trim_available` is not `scope=installed_on_unit`. The dealer's word suffices for condition/options under owner policy.

## 4. Versioned API and event contract

All new APIs use existing auth/tenant claims, TLS, request IDs, idempotency keys on writes and UTC timestamps. Every asynchronous event has the following envelope. Consumers deduplicate by `(producer, event_id)`, tolerate out-of-order delivery and fetch referenced objects rather than trusting stale embedded copies.

```json
{
  "schema_version": 1,
  "event_id": "uuid",
  "event_type": "stock.changed",
  "producer": "dealer-adapter-1",
  "tenant_id": "dealer-7",
  "stock_lifecycle_id": "dealer-7:A104:2026-10-01",
  "occurred_at": "2026-10-11T15:00:00Z",
  "recorded_at": "2026-10-11T15:00:02Z",
  "source_revision": "vendor-sequence-or-hash",
  "trace_id": "uuid",
  "payload_ref": "object-or-record-id"
}
```

Minimum inbound events: `stock.changed`, `stock.sold_or_removed`, `media.batch_completed`, `call.finalized`, `call.qualification_corrected`, `call.transfer_answered`, `crm.appointment_confirmed`, `crm.sale_confirmed`, `crm.other_exit`. Minimum outbound events: `listing.draft_ready`, `listing.needs_input`, `listing.approved`, `listing.publish_requested`, `listing.published`, `listing.live_mismatch`, `listing.withdrawn`, `ml.recommendation_created`. Map actual existing verifier event names to this envelope in the adapter; do not rewrite the verifier's state machine.

**Verifier event payload:** preserve existing `call_id`, tenant, start/end, requested stock candidates with confidence, intent, qualification/reason codes, buyer-stated feature interests and objections, transfer answered state, CRM lead ID, prompt/model/policy version and privacy/consent flags. Emit only after the live decision has completed; logging failure cannot delay transfer. Raw audio and full transcripts remain in their existing restricted store and are not copied into the training warehouse by default. The [core engineering spec](./Core-Media-and-ML-Engineering-Spec.md) gives the proposed JSON example and attribution policy.

Minimum new HTTP endpoints (final path names may conform to the existing app, but behavior must match):

| Endpoint | Request/response contract |
|---|---|
| `POST /v1/capture-batches` | Input stock lifecycle + expected snapshot revision; output batch ID, time-limited per-file upload targets and rights receipt ID. `409` on stock conflict. |
| `POST /v1/capture-batches/{id}/complete` | Input ordered files + declared SHA-256; server verifies bytes and emits `media.batch_completed`. Idempotent. |
| `GET /v1/stocks/{id}/workbench` | Current facts with provenance, media QA, missing inputs, drafts and destination capabilities; scoped to dealer/operator roles. |
| `POST /v1/stocks/{id}/drafts` | Snapshot source revision, queue photo/video/copy generation; output job ID. Repeat with same idempotency key returns same job. |
| `GET /v1/jobs/{id}` | State, step progress, artifact IDs and actionable failure reason; no sensitive raw media URL in logs. |
| `POST /v1/listing-versions/{id}/approve` | Expected version hash + approver identity + destination set; rejects changed source/expired preview. |
| `POST /v1/listing-versions/{id}/publish` | Requires approval token; creates one idempotent job per destination. |
| `GET /v1/listing-versions/{id}/publications` | Provider receipt, external ID, live URL, readback diff and retry/manual state. |
| `POST /v1/integrations/verifier/events` | Signed existing-verifier event; `202` after durable store, duplicate returns prior receipt. |
| `POST /v1/integrations/dealer/{adapter}/events` | Signed/polled stock and CRM normalized event; enforce source authority and tenant mapping. |

Publish an OpenAPI file and JSON Schema/typed definitions for each payload **before** parallel implementation. Generate client/server types from the same contracts. Do not let one agent invent different meanings for `sold`, `qualified`, `approved` or `live`.

## 5. Job state machines and failure semantics

**Stock/listing state:** `unseen → matched → media_received → analyzing → draft_ready → operator_review → dealer_review → approved → publishing → live`, with side states `needs_dealer_fact`, `needs_retake`, `held_conflict`, `publish_failed`, `withdrawal_pending`, `withdrawn`. Store every transition with actor, cause, source revision and timestamp. A current `sold` signal preempts all pending upserts. A price or dealer disclosure change invalidates any unapproved draft and triggers reapproval according to dealer policy. A live version is immutable; replacement creates a child version with rollback pointer.

**Job semantics:** queue jobs are at-least-once, idempotent by tenant + stock lifecycle + source hash + task kind + version. Use retry with exponential backoff for transient vendor/worker failures and dead-letter/operator queue for permanent errors. Atomic object writes use temporary keys then commit after checksum verification. Long renders can be canceled on sold/rights-revoked events. Every task records code version, input hashes, output hashes, duration and reason codes. Workbench shows a precise error such as `VIN_MISMATCH`, `NO_USABLE_VIDEO`, `MISSING_REQUIRED_DISCLOSURE`, `DMS_RATE_LIMIT` or `LIVE_PRICE_MISMATCH`.

**Availability for existing verifier:** expose a read-only, low-latency inventory lookup from the canonical stock state only after proving its freshness and fallback semantics with the existing verifier. A listing worker outage must not make stock appear available. If the verifier already has a better fresh lookup, preserve it and reconcile the two feeds rather than changing the call path.

## 6. UI scope

**Salesperson capture view:** dealer SSO, stock search/VIN scan, visible decoded identity for confirmation, prompted 16-view checklist with category variants, immediate blur/orientation feedback, 20–30 photo target, one or two 45–120 second walkarounds, resumable upload, checksum confirmation and precise retake requests. No ad-copy editor for salesperson. Works on a current iPhone/Android browser with intermittent connectivity.

**Operator workbench:** source fact/attestation panel, market context, original-vs-derivative photo compare at full resolution, suggested hero/order, video contact sheet and clip preview, claim-source view, conflicts, destination preview, model score/uncertainty and override reason. Overrides are logged as labels. Operator cannot change stock price or dealer policy.

**Dealer approval view:** one versioned package showing actual copy, ordered media and destination-specific disclosure/price, with approve/request-changes actions and named approver. Approval is bound to content hash and source stock revision. A changed price, status or required disclosure invalidates the approval. Add routes to the existing Crankshaft site/admin shell when compatible; do not replace its public homepage or call dashboard.

## 7. Media, copy and model implementation

The detailed algorithms, edit recipe, video edit decision list, PyTorch heads/losses, point-in-time feature construction, verifier-to-outcome joins, holdouts and experiment design are specified in [Core Media and ML Engineering Specification](./Core-Media-and-ML-Engineering-Spec.md). The implementation responsibilities are:

- **Photo worker:** immutable ingest, wrong-stock/duplicate/view/quality checks, deterministic real-photo transforms, no fixed sharpening ceiling, set-level gallery selection, original/output comparison and per-channel exports.
- **Video worker:** `ffprobe`, timestamped transcript, scene/quality map, candidate intervals, optional Jev score adapter, constraint-based assembly, FFmpeg EDL renderer, full-export QA and retake reason. Jev ranks; it does not edit the video.
- **Copy worker:** generate only from current dealer-attested facts, price/fees and required disclosure payload. Output structured headline/body/features/CTA plus claim-to-source map; deterministic validator blocks known contradictions and destination violations before review.
- **Photo model:** current [`ml/`](./ml/README.md) starter is untrained. Train on licensed/dealer-authorized editor pairs, compare with rule baseline on whole-dealer/time holdouts, deploy advisory inference behind model version.
- **Outcome model:** join listing-version exposure with verifier qualification and dealer CRM/DMS appointment/sale data. Separate contact rate, qualified-call rate, appointment rate and confirmed retail-sale hazard; never equate delisting with sale. Control for price, promotion, vehicle, dealer, market and channel. Use experiments for claims of improvement.

**Training rights and supply:** the optimistic partner plan assumes signed revenue-share rights for bulk feeds/permitted crawling, text/media processing, model training and lifecycle data. Until contracts and dealer outcomes exist, train presentation rankers only on authorized labels; the 40-listing gallery is not a conversion dataset. Keep a rights lineage and deletion path from each training row/embedding to its asset agreement.

## 8. Dealer integration and publishing adapter contract

At onboarding, complete [Dealer Integration Intake](./Dealer-Integration-Intake.md). Prefer writing the approved record to the dealer's existing inventory syndicator/CMS if it already feeds the website/marketplaces. Direct marketplace adapters are optional and require an authorized route. If no API/feed exists, create a supervised portal task with export package and receipt; do not mark it `live` until checked.

Every adapter implements `discoverCapabilities()`, `readStock()`, `upsert(approvedVersion, idempotencyKey)`, `remove(stockLifecycle)`, `getExternal(externalId)` and `health()`. Capabilities include field limits, disclosures, image/video count/format, update latency, rate limit, price, authentication and acknowledgement semantics. Preserve the dealer's authority: a destination field we cannot represent triggers review, not silent truncation. Check VIN/stock, price, sold status, hero/order, copy, required disclosure and call path on live readback. Record receipt + live snapshot + diff. A sold event cancels queued writes and triggers removals across all connected destinations.

Candidate adapters: independent DMS dealer-approved API/CSV/XML/SFTP/export; franchise DMS partner program; inventory syndicator/website CMS API/feed; marketplace dealer feed/portal; CRM webhook/API/ADF where supported. Confirm the actual product/subscription and vendor terms per dealer. Fortellis's directory is a discovery aid, not a universal DMS endpoint. [Fortellis API directory](https://docs.fortellis.io/docs/general/api-directory-marketplace/api-directory/).

## 9. Work packages for the agentic team

Create one branch/PR per package; parallel work begins after WP-00 contracts are merged. Each PR includes contract tests, migration/rollback notes, observability and a demo fixture. The lead engineer resolves interface conflicts and owns integration testing.

| ID / owner | Dependencies | Deliverable and acceptance |
|---|---|---|
| **WP-00 Architecture/contracts** · lead | Existing repos/access | Actual integration map, architecture decision record, OpenAPI/event schemas, tenant/auth strategy, one end-to-end fixture and CI contract checks. No presumed verifier/DMS fields. |
| **WP-01 Stock/facts** · backend | WP-00 | Inventory adapter, canonical lifecycle/version schema, vPIC cache, dealer attestation/conflict API. Replay of duplicate/out-of-order stock events yields one correct current state; sold preempts draft. |
| **WP-02 Capture** · full stack | WP-00/01 | Mobile stock-select/upload UI, resumable direct-to-object-store upload, hash/rights receipt, progress/retake state. Interrupted upload resumes without duplicate originals. |
| **WP-03 Photo** · media/CV | WP-01/02 | View/quality analysis, deterministic transform recipes, ranking baseline, gallery export and original compare. Golden fixtures prove no wrong-stock, color/condition edits or synthetic substitution. |
| **WP-04 Video** · media | WP-01/02 | Probe/transcript/scene map, candidate clips, EDL, FFmpeg render, captions/audio QA; optional Jev adapter behind feature flag. Fixture reproduces output hashes and does not alter sentence meaning. |
| **WP-05 Copy/QA** · backend/AI | WP-01 | Structured sourced drafts, conflict/price/disclosure validator, destination variants. Every factual claim has dealer/feed provenance; injected unsupported feature fails. |
| **WP-06 Review/approval** · full stack | WP-03/04/05 | Operator and dealer views, content-hash approval, rejection/override audit. Source change invalidates pending approval. |
| **WP-07 Publisher** · integrations | WP-00/01/06 | One authorized syndicator/website route, idempotent upsert/remove, receipt/live readback, mismatch alerts. Pilot stock publish and sold withdrawal proved live. |
| **WP-08 Existing verifier bridge** · integration | WP-00/01 | Signed event ingest from current verifier, stock-interest/qualification/transfer schema, no change to live call latency, existing route behavior regression tests. |
| **WP-09 Outcomes/warehouse** · data | WP-01/07/08 | CRM/DMS appointment/sale adapter, deterministic stock/lead attribution, daily exposure rows, unknown/other exits distinct, point-in-time feature snapshots and audit report. |
| **WP-10 ML baseline/ranker** · ML | WP-03/09 + rights/labels | Train/evaluate existing photo ranker, rules/tabular baseline, whole-dealer/time holdout, model registry/advisory endpoint. No trained model deployed without data-rights and offline gate. |
| **WP-11 Outcome optimizer** · ML/data | WP-09/10 + exposure/outcomes | Exposure-aware funnel/sale model, constrained candidate ranker, uncertainty/calibration, experiment assignment and metrics. No conversion claim before authorized prospective test. |
| **WP-12 Platform/ops** · DevOps/security | WP-00, continuous | CI, migration runner, queues/dead letters, object retention/deletion, tenant isolation, logs/traces, alerts, backups and runbooks. Kill switches per dealer/destination/ML path. |

The team can implement WP-02, WP-03 and WP-04 with fake stock fixtures while WP-01 is built, and WP-08 against recorded/synthetic verifier events. Merge against WP-00 contracts, then run a vertical slice before adding vendors. Do not assign WP-11 before WP-09 supplies trusted denominators and labels.

## 10. Acceptance fixtures, gates and rollout

Check in rights-cleared/synthetic test fixtures: two cars with similar appearance but different VIN/stock, red car with visible dent, panoramic-roof claim conflict, sold-before-publish race, price change after dealer approval, duplicate DMS event, 90-second shaky phone video with one usable scene and one misleading partial sentence, broken provider acknowledgement, failed live readback, buyer call asking about two cars, call with uncertain qualification, confirmed appointment, wholesale exit and true retail sale. Fixtures must contain no real caller PII or unauthorized marketplace photos.

Automated gates:

1. **Unit/contract:** schema compatibility, idempotency, source authority, VIN/provider scope, claim provenance, photo recipe determinism, EDL frame/timestamp validity and tenant authorization.
2. **Integration:** upload → draft → approval → authorized publish → live readback; verifier event → pseudonymous journey → CRM appointment; stock sold while render/publish in flight; destination outage and retry; model service unavailable with rules/manual fallback.
3. **Media/accuracy:** human review of 50 listings and 20 wrong/mixed-car sets with zero invented material claims, known wrong-stock media or altered vehicle condition; inspect original/export pairs and complete clips.
4. **Existing call regression:** replay at least 30 established verifier scenarios, including transfer/no-answer/service/after-hours/consent/failure, and demonstrate the new event bridge adds no material call latency or routing change. Use the existing team's accepted latency SLO as the threshold.
5. **Pilot:** one signed dealer, ten real vehicles, one approved feed/write route, dealer acceptance record, live readback on every version, CRM appointment/outcome receipt, documented processing time and cost. Run new ML in shadow/advisory mode until editor agreement and online evidence justify automation.

Deployment uses dev → staging → one-dealer canary → expanded pilot. Feature flags: `capture`, `photo_auto_suggest`, `video_auto_suggest`, `jev_ranker`, `publish_adapter`, `verifier_event_export`, `ml_ranker`. A kill switch disables any new path without taking down the existing verifier or website. Roll back listings to the last approved version when still current; never republish an old price/status. Observe job backlog, upload/render failures, wrong-stock flags, approval time, publish/live mismatch, call-event lag, attribution coverage, model calibration and dealer correction rate. Each package ships with an operator runbook and ownership of its alerts.

## 11. Definition of done for the engineer

The first production pilot is complete when a salesperson can upload a real car once; Crankshaft creates real polished photos and useful clips, sourced copy and a destination preview; the dealer approves; an authorized adapter publishes and verifies the live listing; a qualified inbound call from the **existing** verifier can be linked to that listing with stated confidence; a dealer-confirmed appointment/sale can flow back as an outcome; and the operator can audit and correct every step. The system must fail into a visible review/manual state when facts, rights, media, vendor access or attribution are insufficient. PyTorch recommendations may be advisory; training and conversion claims require licensed data and measured outcomes.
