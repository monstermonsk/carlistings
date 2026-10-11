# Crankshaft business plan

**Decision document, 11 October 2026.** Crankshaft is the operating company and brand. Listing Tuner is a Crankshaft service. The owner reports that the Crankshaft website, AI verifier and call routing are already built; the new build integrates listing production and outcome learning with those systems. Client footage is edited into useful clips with optional Jev-assisted selection. Crankshaft does not become the seller of a dealer's vehicles.

## Customer and problem

Start with independent used-car dealers that own and advertise their inventory, have a reliable stock feed, use existing listing destinations, and can identify a sales manager responsible for call disposition. Dealer inventory often has generic titles, sparse useful facts, inconsistent imagery, and unprocessed video. Calls can be missed or routed before buyer intent and vehicle availability are known. The offer addresses both the shopper's first impression and the first call. A dealer keeps its DMS, CRM, phone numbers, publishing accounts, prices, and approval authority.

## Offer

1. **Listing Tuner:** ingest authorized inventory; use AI to propose clearer, more useful listing copy; validate every factual claim against dealer records; improve photo presentation without changing the depicted vehicle; select and cut clips from client-supplied video. Publish only through approved paths, then reconcile live listings against source data.
2. **Crankshaft Call Verifier:** answer inbound calls through SignalWire and OpenAI voice, identify the purpose and the relevant vehicle, establish contact and purchase intent, verify availability from a fresh read, route to the right salesperson or fallback queue, and deliver a concise summary into the dealer's CRM. Enrich the caller record **only after** the qualification gate. An unqualified caller is not sent through paid enrichment by default.
3. **Reporting:** listing coverage, publication exceptions, calls answered, qualification outcomes, transfer attempts, answer rate, missed-transfer recovery, AI minutes, decision tokens, costs, and dealer-confirmed outcomes. No attribution or sales-lift claim without a measurement baseline.

## Positioning

Crankshaft sells a managed quality and response layer over a dealer's existing systems. Listing Tuner is a service name, not a stand-alone company, website, or billing entity. The live brand's dark graphite, amber mark, and monospaced cues are used in the local preview. The live Crankshaft website is not modified in this package; the new service page is a ready-to-review local concept for its future update.

## Delivery and account ownership

The dealer supplies the inventory authority, source data, media rights, listing-disclosure instructions, seller contact data, publishing permission, and approved CRM destination. Dealer management owns condition/option statements and its sales-document and salesperson disclosure process. Crankshaft supplies adapters, drafting, QA, media derivatives, call orchestration, analytics, and the account team. The DMS or approved inventory system remains authoritative for stock, price, availability, and sold state. Human dealer sign-off is required for material listing content, image order and publication channels. Call routing rules and enrichment sources require written per-dealer configuration.

## Go-to-market

Use a paid ten-vehicle proof with a measured before/after audit and test calls before selling a recurring plan. Prioritize dealers with one inventory source, one listing write path and one CRM handoff. Demonstrate three outcomes: accurate stock/price propagation, materially better listing usefulness, and a qualified call reaching the assigned human. Retain the established **$795 / $1,295 / $1,995 monthly prices** for **30 / 60 / 100 active listings**, respectively. Proposed included AI verifier minutes are **750 / 1,500 / 2,500**, or 25 per active listing, with token cost inside the plan; customers needing more recurring capacity upgrade plans rather than receive a separate usage bill. These minute allowances require pilot validation before contract commitment. Define the minute counter and human fallback in each contract. Specialty vehicles can follow only after automotive operations are repeatable.

## Operating plan

- **Weeks 1–2:** inspect existing website/verifier/routing contracts; signed dealer scope; source mapping; inventory snapshot; approval policy; baseline metrics and event schemas.
- **Weeks 3–4:** one inventory adapter, capture and copy/photo/video workbench, human QA, authorized publication path, and event bridge from the existing verifier to listing analytics.
- **Weeks 5–6:** paid pilot on ten vehicles, regression tests of existing call routing, dealer CRM/outcome joins, publication and rollback drills, and dealer acceptance.
- **After pilot:** open additional vendor adapters and plans only when the actual economics and delivery hours fit the business model. Do not project scale from one integration.

## Data partnership and machine-learning expansion

The upside plan assumes revenue-share agreements with listing-site owners grant bulk download or permitted crawling, plus rights to retain, label and train models on listing text, photos and video. Pursue 100,000–250,000 licensed listing lifecycles across partners as an initial scale target. Seek listing-level exposure and outcome data in the same contracts so Crankshaft can learn which presentation generates qualified buyers, not just mimic visible listings. The existing AI verifier can supply structured buyer intent, questions, objections and qualification outcomes; dealer CRM/DMS events can confirm appointments and retail sales. These must be linked to the live listing version with stated attribution confidence. Partner share becomes a distinct data-acquisition cost in unit economics. If partner outcome data is unavailable, use that corpus for visual/editorial labels and rely on dealer pilots for conversion evidence. [Core media and ML engineering specification](./Core-Media-and-ML-Engineering-Spec.md) defines the joins, training labels, models, holdouts and experiments.

The dealer field process is intentionally light: identify the stock/VIN, confirm the car, take prompted photos and a phone walkaround, and upload. Crankshaft owns VIN lookup, dealer attestation intake, ordinary media processing, copy, review, authorized delivery to the dealer's inventory software and distribution channels, and post-publication reconciliation. We take the dealer's word for condition and options, highlight positives and do not make obvious statements we know are false. Offer a free vPIC lookup by default, use dealer-owned decoder accounts where permitted, and budget an optional OEM/build-data provider when useful. Dedicated adapters target the dealer's syndication hub first, then approved platform feeds and portals. Cars launch first; category adapters later handle trucks, RVs, trailers, boats and powersports.


## People and controls

Account lead owns dealer relationship, scope and approval. Listing editor owns factual copy and photo QA. Video editor owns deterministic cuts and output inspection; Jev ranks candidate clips. Integration engineer owns tenant adapters and reconciliations. Call operations owner reviews misroutes, transcript issues, transfer outcomes and spend. Small teams can combine roles, but the same person should not approve their own material change without a dealer approval record.

Store originals, sources, versions, approval actors, and decision logs. Isolate dealer data by tenant. Capture only the minimum caller data needed for qualification and handoff; implement opt-out, retention and recording/consent rules per jurisdiction and dealer policy. Do not assert a uniform recording-consent rule across states. Include a clear human fallback and emergency-call behavior. Any failed fact check, stale availability, unclear caller consent, or connector failure must stop the affected automation and surface an operator task.

## Success measures and gates

Gate 1: zero invented material facts and zero altered-condition photos in a 50-listing QA set; 100% approved price and stock matches on pilot publications. Gate 2: at least 95% of pilot test calls produce a correct intent classification or safe fallback; every attempted transfer and cost is logged. Gate 3: dealer confirms CRM receipt of all test leads with no cross-tenant data leakage. Gate 4: measured gross contribution remains positive under the 30k-token stress case and actual inclusion mix. Track lead-to-appointment and sale only if the dealer returns outcome data; compare with a pre-pilot baseline.

## Principal risks

Measure actual 30,000-token verifier decisions and call length before committing to allowances. Marketplace and DMS access varies by dealer; use contracted feeds and approved routes. Jev ranks candidate moments; editors cut and inspect the clips. Recheck stock before publication and each relevant call. Keep human fallbacks for stale data and failed transfers.
