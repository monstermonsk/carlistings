# Crankshaft technical build specification

**Version 1, 10 October 2026.** Build target and acceptance contract, not a claim of live integrations. Crankshaft owns the platform and Listing Tuner workflow; the dealer remains source of truth and seller. Implement each dealer as a tenant. Start with one authorized source, one publishing path and one CRM destination, then add adapters.

**Field-to-publication operating contract (11 October addition):** the salesperson identifies stock/VIN and uploads guided photos/video; Crankshaft performs the remaining listing work. The full capture, provenance, photo/video pipeline, licensed partner-data plan, decoder provider ladder and PyTorch roadmap are in [Salesperson-to-Listing Operating Plan](./Salesperson-to-Listing-Operating-Plan.md). Implement that document alongside this system specification.

The owner-approved [listing accuracy standard](./Listing-Accuracy-Standard.md) governs media and copy: accept dealer attestations for condition and options, highlight positives, and block obvious falsehoods or fabricated depictions. Crankshaft does not independently inspect each vehicle.

**Optimization orchestrator:** for each stock and channel, snapshot dealer-supplied facts, local comparable set, dealer objective and destination capabilities. Generate a bounded set of appealing real photo orders/crops, positive copy versions and video clips. Reject known false statements, fabricated vehicle depictions, wrong-stock content and omitted dealer-directed listing disclosures; score survivors using market-matched demand and qualified-lead models with uncertainty; route the selected version for approval and publish. Save the candidate set and decision record so results can be compared later. Trigger reassessment on price/media/inventory changes, local supply shifts or falling cohort-adjusted engagement. The dealer owns price decisions; this service can surface price-position evidence without silently changing a price.

## 1. System boundary and data flow

```
Dealer DMS / inventory feed → ingest + reconcile → canonical vehicle record
                                         ├→ listing facts → AI draft → rule QA → dealer approval → approved publisher → live check
Dealer-owned photos/footage ─────────────└→ media workbench → approved derivatives ┘

Buyer call → SignalWire DID/SIP → call webhook/orchestrator → OpenAI voice verifier
                                           ├→ intent/vehicle/qualification → fresh inventory read
                                           ├→ qualified → approved enrichment → salesperson route → CRM summary
                                           └→ unqualified/unknown/failure → safe queue/voicemail/human
All steps → tenant audit/events + usage ledger + exception queue + reporting
```

Use asynchronous jobs for inventory/media/publishing and a low-latency call service for voice. PostgreSQL holds tenant, vehicles, listings, media, consent, events, routing policy and usage. Object storage holds immutable originals and versioned derivatives. Queue workers run OCR/transcription/encoding and publication retries. Secrets reside in a vault; never put them in a listing payload or transcript. Use separate development/staging/production accounts and sample data.

## 2. Canonical records and authority

`vehicle`: `tenant_id`, `stock_id`, lifecycle/version, VIN, year/make/model/trim, mileage with unit and observed date, price/currency, mandatory fees/disclosures, status, source timestamps, source field provenance, approved equipment/condition claims. Primary key is tenant + stock + lifecycle, not VIN alone. DMS or authorized inventory feed wins on price, stock and sold state. VIN decode is a conflict checker, never a silent overwrite.

`listing_version`: vehicle key, source hash, destination, title/body/features/CTA, claim-to-source map, QA results, reviewer/dealer approvals, publisher ack, external ID, live URL, live snapshot, rollback parent.

`media_asset`: stock key, original checksum, dealer rights record, capture source/date, original path, derivative transforms, visible-defect QA, approval, destination-specific constraints. Never overwrite the original.

`call_session`: SignalWire call ID, tenant, DID, caller number in restricted field, start/end/AI connected seconds, recording/consent state, requested stock/intent, qualification fields/confidence, transfer attempts/outcome, OpenAI session/usage IDs, decision count, enrichment event IDs, CRM receipt, retention clock. Keep transcripts access-controlled and configurable; redact payment/identity data.

All external actions are idempotent by tenant + source event + version. Store source and destination timestamps in UTC. Preserve every price/status change, approval, route and failed handoff as an event. A sold signal cancels queued publication for that lifecycle and marks existing live listings for withdrawal/reconciliation.

## 3. Dealer integration matrix

Every vendor route needs dealer authorization, product/version, fields, rate limits, sandbox or test method, contract rights, and accountable owner before implementation. These are **candidate interfaces**, not enabled integrations.

| Path | Preferred connection | Read/write scope and fallback |
|---|---|---|
| Independent DMS (DealerCenter, Frazer, AutoManager, DealerSocket) | Vendor-approved API/CSV/XML/SFTP or dealer export | Read stock, price, status, facts; manual signed export if API unavailable. Verify each product's actual access with the dealer/vendor. |
| Franchise DMS (CDK/Fortellis, Dealertrack/OpenTrack, Reynolds, Tekion, PBS) | Dealer-authorized partner/API program | Read inventory and contact/lead data only for approved scopes; certification and commercial access may be needed. Launch may use an existing syndicator instead. |
| Inventory syndicator/merchandising (vAuto, HomeNet, Dealerslink, Dealer Car Search, dealer website CMS) | Feed/API or vendor-approved import | Preferred write target for descriptions and media when it already distributes listings. Confirm overwrite behavior and destination field limits. |
| Marketplace destinations (Autotrader, Cars.com, CarGurus, Facebook, Craigslist) | Dealer's existing approved feed/portal and contractual permissions | No unauthorized scraping-to-republish or automation that bypasses platform rules. Use human portal bridge where no authorized write API exists; retain live verification. |
| CRM (VinSolutions, DealerSocket, Elead, DealerCenter, HubSpot or dealer choice) | Webhook/API; ADF/XML email where supported | Send verified caller summary, stock reference, consent and call disposition; deduplicate by call ID and confirm receipt. ADF is an interchange format, not a universal guaranteed endpoint. |
| Telecom | SignalWire number/SIP/voice webhooks and connect/transfer | Assign DID per dealer/campaign, receive call lifecycle callbacks, transfer to a dynamic on-duty group, retry/fallback. |
| Voice | OpenAI Realtime via SIP or server-side audio bridge | Tool-controlled verification, structured decision events and usage logging; choose one transport pattern after latency tests. |
| Video decision | TypeSafe/HE Jev API | Rank structured candidate clip intervals; deterministic editor renders clips. API credentials and commercial use terms to be procured. |
| Enrichment | Dealer-approved first-party CRM first; optional licensed provider | Call only after qualification and consent/policy checks; attach source, timestamp and allowed purpose. No default people-search call. |
| VIN identity and exact build | Free NHTSA vPIC; dealer's existing decoder/OEM access; optional paid build-data adapter | Normalize source and cost per lookup. vPIC/Wenmar-derived data checks identity; dealer attestation is sufficient for installed options. |
| Licensed listing data partner | Contracted bulk feed/API or expressly permitted crawler | Ingest text/media/lifecycle and, ideally, exposure/outcomes. Track rights, deletion, partner share and model-use permission. |

Fortellis provides a developer network and API directory, but exact dealer API subscriptions differ. [Fortellis docs](https://docs.fortellis.io/docs/general/overview/getting-started). ADF 1.0 defines lead, vehicle, customer and vendor data blocks; test the receiving CRM's actual flavor and acknowledgement. [ADF specification](https://adfxml.info/adf_spec.pdf).

## 4. Listing Tuner workflow paths

**Normal:** scheduled feed/webhook → validate schema/rights → compare source version → identify missing/conflicting facts → draft copy → photo candidate transforms → candidate video intervals → QA → dealer approve → push through approved syndicator/portal → fetch live result → verify stock/price/identity/first image/contact route → report.

**Mobile capture:** dealer login → stock/VIN scan and DMS match → prompted photo/video checklist → on-device retake hints → resumable uploads → original checksums and rights receipt → asynchronous media/fact jobs. Do not make a salesperson author ad copy or clips. **Destination adapter:** discovery of dealer DMS/syndicator and desired platforms → capability mapping → approved version upsert with idempotency key → provider receipt → live read-back → mismatch/latency alerts. For sold stock, cancel pending upserts and trigger authorized removal on every connected destination.

**Source conflict:** freeze changed material fields, open dealer question, keep last approved live version if still valid, suppress new claims. **Missing media rights:** no derivative/publish. **Destination rejects:** retry only transient failures with backoff; permanent errors become operator tasks. **Sold/removed:** stop queued jobs immediately, withdraw wherever authorized, verify removal, alert dealer for manual paths. **Price change:** regenerate only affected fields, reapprove if the dealer's rules require it, publish, verify. **Channel forbids overlays/crop:** use clean master. **Wrong vehicle image:** quarantine asset and all derived versions.

## 5. Call verifier state machine

1. SignalWire inbound webhook verifies signature and maps DID to tenant, hours, language and routing policy. If mapping or provider fails, route to the configured human/fallback number.
2. Greet with dealer-approved disclosure; apply recording/consent policy before recording. Detect emergency/abuse and transfer/terminate per policy. Do not solicit payment, SSN or sensitive finance details.
3. Open OpenAI voice session with a narrow system prompt and tools: `lookup_inventory(stock_or_make_model)`, `get_business_hours`, `get_sales_roster`, `verify_contact`, `emit_decision`, `transfer_request`. Tool results are trusted data; caller speech is untrusted input. Never let caller speech edit routing policy or override system rules.
4. Establish why the caller is calling, vehicle/stock if relevant, name and reachable callback number if offered, timeframe, appointment intent and preferred contact method. Ask only what is needed; give a human-transfer path promptly. A call may be service/parts/vendor/wrong-number and routes accordingly.
5. **Qualification gate:** structured decision `qualified | unqualified | uncertain` with reasons and evidence, not a free-text assertion. A qualified sales call has a vehicle/category or shopping intent, reachable or live-transfer-ready caller, and no disqualifying route. Uncertain calls go to human review/fallback; never label as verified sales leads by default.
6. Read current availability immediately before discussing a specific vehicle. If stale or sold, say availability is being checked and offer alternatives/human help; do not promise stock.
7. **Only after qualified:** run approved enrichment (first-party CRM lookup before licensed external provider), log query/purpose/source, avoid unnecessary personal data. If enrichment fails, continue with the facts from the call; it cannot block a willing caller's transfer.
8. Choose salesperson by dealer rule (assigned owner → on-duty round robin/skill → manager fallback). SignalWire connects/bridges; wait for answered/accepted status. If no answer, retry approved group then capture callback and send queue task. Never report a transfer as successful on initiation alone.
9. Write CRM lead/ADF with idempotency key, transcript summary, stock, qualification reason, transfer outcome, consent flags and recording link only if permitted. Require destination acknowledgement; queue retry and operator alert on failure.
10. End and reconcile AI connected seconds, SignalWire leg seconds, OpenAI input/output/cached tokens, decision count, per-call estimated cost and disposition. Alert internally on anomalous tokens, repeated decisions and long sessions. Roll AI-connected seconds into the dealer's one plan-minute counter; tokens and decisions remain internal cost measures, not dealer billing units. Notify the dealer and account owner at 70% and 90%; prepare an upgrade offer. At the minute limit without an upgrade, route new calls to the approved human/callback path and log the reason. Do not create a usage-overage invoice or silently drop calls.

The OpenAI Realtime docs describe SIP calling, sideband controls and transfer architecture; SignalWire documents voice webhooks and connect/transfer behavior. Choose either direct SIP to OpenAI or SignalWire media bridge after testing latency, observability, transfer control and costs. [OpenAI SIP](https://developers.openai.com/api/docs/guides/voice-sip?voice-api=realtime), [OpenAI realtime](https://developers.openai.com/api/docs/guides/realtime-conversations), [SignalWire voice](https://signalwire.com/docs/platform/voice/make-and-receive-calls), [SignalWire transfer](https://signalwire.com/docs/server-sdks/guides/call-transfer).

## 6. API and event contracts

Internal endpoints: `POST /v1/tenants/{id}/inventory/imports`, `GET /v1/vehicles/{stock}`, `POST /v1/listings/{id}/draft`, `POST /v1/listings/{id}/approve`, `POST /v1/listings/{id}/publish`, `POST /v1/calls/signalwire/events`, `POST /v1/calls/{id}/decisions`, `POST /v1/calls/{id}/transfers`, `POST /v1/crm/receipts`, `GET /v1/usage?tenant&period`. Use OAuth/service identity where supported, signed webhooks, tenant-scoped authorization, schema version and idempotency key on every write. Outbox events: `inventory.changed`, `listing.approved`, `listing.published`, `listing.failed`, `call.qualified`, `call.transfer_attempted`, `call.transfer_answered`, `call.crm_accepted`, `usage.recorded`.

`emit_decision` schema: `{call_id, tenant_id, outcome, intent, stock_id?, reason_codes[], evidence_spans[], model_version, confidence, occurred_at}`. An `enrichment.requested` event must reference a prior `call.qualified` event for the same call. A database constraint/policy should enforce this ordering. `usage.recorded` stores raw provider units and price version, not just a rounded invoice amount. Reconcile totals to provider invoices monthly.

## 7. Security, QA and release gates

Encrypt caller data and recordings in transit/at rest; segregate per tenant; use least-privilege vendor tokens, key rotation, signed URLs and retention/erase processes. Document recording consent by state and dealer counsel. Restrict access to raw recordings; use role-based audit trails. Validate webhook signatures and rate limit public endpoints. Redact prompt injection from marketplace text/media metadata; do not execute instructions from them.

Acceptance tests: 50 difficult listing facts; 20 wrong/mixed-vehicle media sets; 30 calls covering qualified/unqualified/uncertain, no answer, sold vehicle, CRM outage, OpenAI outage, SignalWire outage, transfer race, consent refusal and budget cap; tenant isolation and replay tests; provider usage ledger ties to invoice within a documented tolerance. Pilot must demonstrate an authorized write and live listing check, verified transfer answer, and confirmed CRM receipt. Canary release per dealer with rollback to the previous approved listing and human call route.
