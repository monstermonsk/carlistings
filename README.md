# Crankshaft | car listings and verified calls

Updated 11 October 2026. **Crankshaft** is the company and customer-facing brand. **Listing Tuner** is its managed listing service. This repository contains the current launch and build package; historical materials are excluded.

## Open these first

- [Launch package](./START-HERE.html): local branded hub and navigation. Download or clone the whole repository before opening it so linked pages remain together.
- [Dealer-facing sample website](./website/index.html): separate offline concept for the Crankshaft website update.
- [Business plan](./Business-Plan.html): market, offer, operations, rollout, risks, and validation gates.
- [Business model](./Business-Model.html): restored $795 / $1,295 / $1,995 prices, proposed AI minutes, plan upgrades, and unit economics.
- [Investor brief](./Investor-Brief.html) and [dealer sales kit](./Sales-Kit.html): concise commercial materials for launch conversations.
- [24-month financial model](./financials/Crankshaft-24-Month-Model.xlsx) and [model guide](./financials/Model-Guide.md): editable account, minutes, token cost, profit and cash forecast.
- [Technical build specification](./Technical-Build-Spec.html): engineer handoff with existing-system boundary, APIs/events, state machines, work packages, fixtures and release gates.
- [Connector catalog and dealer portal specification](./Connector-Catalog-and-Dealer-Portal-Spec.html): researched DMS/CRM/marketplace routes, secure token setup, Crankshaft salesperson directory, call-to-agent ledger, standardized adapters and CSV fallback.
- [Core media and ML engineering specification](./Core-Media-and-ML-Engineering-Spec.html): photo/video algorithms, verifier and dealer outcome joins, PyTorch models, labels and experiments.
- [Copy-ready agent team brief](./engineering/AGENT-TEAM-BRIEF.html), [handoff guide](./engineering/README.html) and [starter OpenAPI](./engineering/contracts/listing-api.openapi.yaml): execution order and machine-readable contracts.
- [Media production specification](./Media-Workflows.html): detailed text, truthful photo, and Jev-assisted video workflows.
- [Salesperson-to-listing operating plan](./Salesperson-to-Listing-Operating-Plan.html): automatic best-feasible listing loop for each car and local market, guided capture, VIN/build-data ladder, truthful media, dealer-system publishing, licensed partner data and PyTorch roadmap.
- [Listing accuracy standard](./Listing-Accuracy-Standard.html): owner-approved rule for dealer attestations, positive merchandising, required disclosures and blocking obvious false statements.
- [Developer starter](./ml/README.md): free vPIC adapter and untrained PyTorch photo ranker/training script.
- [Dealer service guide](./Dealer-Service-Guide.html): current offer and client-facing scope.
- [Dealer connection setup](./Dealer-Integration-Intake.html) and [launch checklist](./Launch-Checklist.html): standard self-service provider/roster setup and release gates.
- [40-listing review gallery](./samples/index.html): source-photo placeholders, scored listing cards, specific suggestions, and proposed copy. The source links may change because listings are live inventory.
- [Research and assumptions](./Sources-and-Assumptions.html): dated vendor and market sources; separates observed rates from proposed pricing.
- Print-ready PDFs: [business plan](./plan/Crankshaft-Business-Plan.pdf), [business model](./plan/Crankshaft-Business-Model.pdf), [investor brief](./plan/Crankshaft-Investor-Brief.pdf), and [dealer service guide](./sales/Crankshaft-Dealer-Service-Guide.pdf).

The gallery is an internal research artifact, not a set of dealer-authorized publications. The public gallery omits third-party marketplace thumbnail files. Do not publish rewritten listings or dealer media without rights and fact approval. No sample videos were edited.

## Current status

The owner reports that the **Crankshaft website, AI verifier and call routing already exist outside this repository**. Their code, credentials and exact event contracts are not present here; the new build integrates with them. The Crankshaft-side dealer portal, staff database, call ledger, standardized vendor connectors, Listing Tuner media processing, dealer publishing, outcome warehouse and trained models are design/build work, not deployed integrations. The connector catalog distinguishes documented APIs from partner-gated feeds and human submission paths; it does not claim Crankshaft has vendor credentials today. The original monthly prices are restored. The proposed minute allowances require pilot cost data before quoting as fixed commitments. The owner reports about 30,000 total measured tokens per verifier decision; the audio/text split and representative number of decisions per call still need to be measured.

This public repository omits third-party marketplace photo files; the 40 listing grades, draft text, suggestions and source links remain available for review.

