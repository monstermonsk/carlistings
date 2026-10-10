# Crankshaft investor and operator brief

**October 2026 planning draft.** Crankshaft combines its inbound call verification and routing workflow with Listing Tuner, a managed vehicle listing service. Listing Tuner is a service under Crankshaft, not a separate brand or seller. The dealer keeps its inventory, publishing accounts, CRM and final approval.

## Offer and differentiation

The workflow improves the vehicle page and the call it generates. AI proposes listing copy from dealer-verified facts, supports truthful photo presentation and helps select moments from client footage through Jev. An editor renders and reviews clips. SignalWire carries inbound calls, OpenAI voice establishes intent and buyer context, current inventory is checked, and a qualified caller reaches an available salesperson. Enrichment occurs after the qualification gate. The CRM receives a summary and transfer outcome.

The commercial advantage depends on dealer execution quality and measurable handoffs, not on a claim that generic AI reception is novel. Crankshaft must prove accurate listings, useful call qualification and answered transfers at pilot scale.

## Proposed economics

Launch / Growth / Scale retain the established **$795 / $1,295 / $1,995 per month** prices, with **750 / 1,500 / 2,500** included AI verifier minutes: 25 minutes per active listing across 30/60/100 listings. There is **no separate minute, decision or token charge**; a dealer needing more ongoing capacity upgrades plans. Listing Tuner throughput remains 20/40/70 rebuilt listings and 10/25/50 client-footage clips. A $495 ten-vehicle pilot is credited toward month one under the stated terms. The minute allowances require pilot cost validation before they are committed in contracts.

The owner's **30,000 total measured tokens per verifier decision** is a major cost variable. The audio/text split is not known. At the published `gpt-realtime-2.1` rates and an illustrative 24k input/6k output split, one decision costs about **$1.15 if all tokens are audio** or **$0.24 if all are text**. The workbook uses the audio case and one decision per three-minute call for stress testing. SignalWire's US inbound transport starts at $0.0066/minute; a bridged outbound PSTN leg adds $0.008/minute. These supplier costs are absorbed in plan pricing. [OpenAI pricing](https://developers.openai.com/api/docs/pricing); [SignalWire pricing](https://signalwire.com/pricing).

The editable [24-month model](./financials/Crankshaft-24-Month-Model.xlsx) projects $121,555 Year 1 revenue with a $74,325 operating loss, then $465,536 Year 2 revenue with $9,224 operating profit. It assumes rapid dealer additions, a fixed plan mix, 2% monthly churn and **18% of included AI minutes used**, with no voice overage or plan-upgrade revenue. Its simplified $50,000 opening cash is negative by about $24,325 at Year 1 end, so this scenario needs more funding or lower fixed costs. At full included-minute use, the current price and full-audio cost case has negative direct margin; this is a launch risk requiring pilot measurement before capacity is contracted. Cash timing, taxes, integration fees and capex remain outside the model.

## Pilot gates

First dealer: one authorized stock source, one approved publication path, one CRM destination, a routing roster, and clear media/recording rights. Deliver ten approved vehicle examples and at least 30 call tests covering transfer and failure paths. Do not open a second integration wave until the dealer accepts the published facts, transfer outcomes reconcile, CRM receipts are confirmed and actual tokens/editor time fit gross margin targets. The technical spec defines these checks.

## Main risks

Vendor access and marketplace write rights differ per dealer; do not sell a universal connector. Vehicle price/availability can change between listing and call, so make fresh reads. Photo and video editing must preserve actual condition. A voice classifier can misroute callers; the human fallback and exception queue are part of the service. The strongest commercial risk is underestimated voice usage at 30k tokens per decision, followed by high labor for media review. These are measurable in a paid pilot.
