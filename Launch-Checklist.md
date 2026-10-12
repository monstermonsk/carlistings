# Crankshaft launch checklist

| Gate | Owner | Evidence before completion |
|---|---|---|
| Brand and offer approved | Founder | Crankshaft logo, Listing Tuner service name, plan terms and current local site approved |
| Dealer pilot signed | Account lead | Scope, title/ownership authority, data/media rights, approval contacts and billing terms |
| Mobile capture rehearsed | Listing lead | Salesperson can scan stock/VIN, collect prompted views and video, and complete a resumable upload without writing copy |
| Decoder sources mapped | Integration lead | vPIC response reconciled to DMS; dealer-owned or paid build-data permissions, installed-option coverage and per-lookup cost recorded |
| Destination map approved | Integration lead | Dealer DMS/syndicator, each marketplace route, write permission, field limits, acknowledgements and live-readback method recorded |
| Site automation approved | Automation lead | Existing Crankshaft runtime mapped; dealer/site permission for each workflow, duplicate suppression, login/MFA pause, submission evidence, live check, UI-change halt and sold withdrawal tested |
| Partner dataset contracted | Founder + data lead | Site-owner revenue share, bulk download/crawl scope, media/model rights, deletion rules and exposure/outcome fields documented before partner-scale training |
| System access authorized | Integration lead | Vendor account permissions, sandbox/test route and credential vault entries |
| Inventory mapped | Listing lead | Stock/price/status/fees/mileage provenance and sold-event test |
| Media intake passed | Media lead | Original checksums, stock match, rights, dealer-requested condition views and destination formats |
| Copy and photo QA passed | Editor + dealer | Dealer-attested claims, no known falsehood or fabricated vehicle edit, required disclosures, approved version and live check |
| Jev clip workflow passed | Video editor | Candidate score log, deterministic edit list, complete visual/audio review and approval |
| Existing SignalWire route regression tested | Call lead | New event bridge leaves normal/after-hours/service/emergency/fallback and transfer-answer behavior unchanged |
| Existing OpenAI verifier bridge tested | Call lead | 30-call edge-case replay, structured buyer-interest events, inventory freshness and no added live-call latency |
| Enrichment gate tested | Privacy owner | External lookup only after qualified event, consent/policy check and purpose log |
| Dealer portal and CRM/CSV paths tested | Integration lead | Staff directory, attempted/answered agent call ledger, idempotent CRM lead receipt where authorized, CSV export fallback, retry and cross-tenant isolation proof |
| Listing-to-call feedback joined | Data lead | Existing verifier event maps to the live listing version with stock-match method/confidence; unattributed calls remain separate |
| Dealer outcomes joined | Data lead | Appointment and confirmed retail-sale receipts distinct from wholesale, transfer and unknown removal |
| ML gate documented | ML lead | Rights-cleared labels, dealer/time holdouts, rules baseline and shadow-mode evaluation before any automatic recommendation |
| Billing tested | Finance owner | AI-connected minutes reconciled to SignalWire/OpenAI logs; token cost kept internal; no usage overage line; upgrade alerts and human fallback tested |
| Support and rollback ready | Operator | Alert recipients, outage route, listing rollback and customer contact path |
| Pilot accepted | Dealer + founder | Agreed factual, call, cost and reporting criteria recorded |

No checked box is a substitute for evidence. A failed path stays in test or manual operation while unaffected paths may continue under the dealer's approved scope.
