# Crankshaft listing accuracy and disclosure standard

**Approved business rule, 11 October 2026.** The goal is more qualified buyers and sales by presenting each car in its best light. Listing Tuner does not knowingly make false statements; an online listing is marketing content, not the sales contract; and the dealer is the source of truth for condition and installed options. Dealer management decides which disclosures belong in each listing and handles its own sales documents and salesperson duties. Crankshaft implements the dealer's content instructions. This document allocates workflow responsibility; it does not declare that advertising law cannot apply to Crankshaft. The [FTC Used Car Rule guide](https://www.ftc.gov/business-guidance/resources/dealers-guide-used-car-rule) and [FTC advertising guidance](https://www.ftc.gov/business-guidance/resources/automobile-industry-pricing-transparency-faqs) show why a sales contract and an ad should be treated separately.

## Exact definition

**A Crankshaft listing is acceptable when it presents the actual unit attractively, uses dealer-approved claims and offer terms, follows the dealer's instructions for that channel, and contains no obvious statement or visual edit Crankshaft knows is false.** Dealer statements are sufficient for condition and options. Crankshaft does not independently inspect or warrant those facts. It selects the most appealing real views and positive claims. If Crankshaft sees a direct conflict in its own data or media, it asks the dealer to resolve it before publishing that claim.

**Image rule:** listing photos are real photos of the dealer's actual car. Crop, straighten, adjust lighting, denoise and sharpen them as much as is useful for presentation. AI may help choose the photos and edit settings. Do not remove dents or damage, change the car's color, parts or condition, or replace the real capture with an AI-created depiction. No generative reconstruction, inpainting, synthetic background or composite of another vehicle is published as a photo of this unit. Keep the original so the dealer can compare it with the export. The same rule applies to vehicle video frames.

“Knowingly” includes facts already present in Crankshaft's own record and obvious contradictions surfaced by automated or human review. This standard does not authorize ignoring a known conflict. It also does not promise a complete catalog of every scratch, option or mechanical issue. The dealer decides what to disclose on the listing and in its sales process; Crankshaft records and follows those instructions.

## Pass/fail rules for the workflow

| Area | Pass | Hold or reject |
|---|---|---|
| Identity | Stock/VIN and photographed vehicle match the dealer's unit. | Known wrong car, mixed-car media or unresolved identity conflict. |
| Price and status | Use current dealer-authorized advertised price, mileage, availability, fees and terms; refresh when the dealer changes them. | Knowingly stale price or sold status, invented terms, or a destination that strips a required offer disclosure. |
| Options | Dealer-attested installed options are publishable; an OEM/build sheet can enrich or cross-check them. Record who attested and when. | Claiming a generic decoder's “available” option is installed without dealer attestation or other unit-specific evidence; publishing after the dealer retracts the option. |
| Condition and history | Use the dealer's condition, accident/history, title, warranty and certification statements as given. Carry over each item the dealer marks as a required listing disclosure. | Inventing “accident-free,” “flawless” or “certified”; omitting a dealer-marked required disclosure; contradicting a dealer-supplied condition record. |
| Photos | Choose attractive real angles and order; rotate, crop, correct lighting, resize, denoise, sharpen to the desired finish and blur private information. Preserve the vehicle's actual appearance and the original file. | Digitally removing dents/damage, changing color, parts or condition, or presenting an AI-created/stock image as this actual unit. A hero photo need not show every disclosed flaw. |
| Video | Cut real footage into short clips, stabilize, crop, caption and normalize audio without changing the meaning of a factual statement. A clip need not show every defect. | Fabricated vehicle footage, false captions/narration, or an edit that changes a spoken claim's meaning (for example, removing “does not work”). |
| Copy | Draft from dealer attestations, inventory data and other recorded sources. Marketing language may be concise and selective. | A factual claim Crankshaft knows is unsupported or contradicted; an AI-invented feature, history, price or scarcity claim. |
| Dealer-directed disclosures | Dealer provides a per-unit payload stating what belongs in the online listing for each destination; Crankshaft maps it and checks the live result. | Crankshaft omits an item the dealer instructed it to publish, or invents a legal disclosure rule without dealer direction. |

## Dealer attestation and system of record

At onboarding, the dealer names the person or feed authorized to attest to **condition, installed options, history, warranty/certification and required disclosures**. A structured attestation includes stock/VIN, value or disclosure text, staff identity or source feed, timestamp and revision. One dealer attestation can cover a set of fields; Crankshaft need not demand a build sheet for each option or independently inspect the car. VIN decoders provide candidates and conflict prompts, not a substitute for the dealer's unit-specific statement. When a decoder and dealer disagree about an option, ask for dealer confirmation; a generic decoder does not automatically override the dealer.

The DMS/inventory feed remains the operational source for stock, price, mileage and sold status, subject to the dealer's integration map. Dealer management determines which items belong in the online ad, Buyers Guide and sales contract for each market and channel. Crankshaft does not infer that every contract clause must appear online, nor does it decide the dealer's legal duties. If an item the dealer instructed us to publish cannot fit a destination, route it back for an approved channel-specific solution rather than silently dropping it.

## Practical examples

1. **A car is red in the source media and dealer record.** Describe and present it as red. Do not recolor it gray or call it gray. Correcting the camera's white balance while keeping its real red color is allowed.
2. **Dealer says the car has a panoramic roof.** We can list it after recording the dealer's attestation; no paid VIN build sheet is required. If the uploaded photos clearly show a solid roof, ask the dealer to resolve that conflict first.
3. **Dealer instructs us to mention a prior accident and repaired front bumper online.** Carry that wording into each applicable listing version. A polished hero angle may show the car at its best; no need for every shot to show the repaired area. Do not digitally erase damage visible in a chosen source photo.
4. **Dealer says a small dent is handled in its sales documents and does not direct us to describe it online.** We do not independently inspect for other dents or add that statement on our own. If the salesperson uploads a dent photo, do not digitally remove it.
5. **VIN service lists heated seats as standard/available; dealer does not confirm them.** Do not assert heated seats based on that decoder alone. Ask the dealer or omit the claim.
6. **A price changes before publication.** Pull the dealer's current price, regenerate the affected listing version and obtain the configured approval. Do not publish the known old price.
7. **A phone clip says “the air conditioner does not cool.”** We may omit that entire segment if the dealer's required disclosures are still carried; we may not cut only “does not” and publish a false claim.
8. **Background cleanup.** Cropping lot clutter is allowed. Replacing the lot with a showroom and passing it off as a real scene is rejected; a separately labeled promotional graphic is a different asset.

## Approval and audit

Crankshaft keeps original media hashes, edit decisions, dealer attestations, required-disclosure payloads, approved listing versions and live destination snapshots. The normal launch flow is automated draft/QA, Crankshaft exception review and dealer-configured approval before publication. Later low-risk automation can be enabled by dealer instruction and measured audit performance. A discovered error triggers correction or withdrawal across affected destinations and a record of the fix.

**Owner-approved direction:** dealer attestation is enough for condition and options; Crankshaft is not the truth police or the seller; dealer management controls online disclosures and salesperson sales-document duties; we promote the vehicle's positives and block obvious falsehoods or fabricated depictions, while allowing attractive selection, ordinary editing and selective copy. Changes to this rule should be versioned and approved by the owner.
