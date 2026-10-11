# Crankshaft core media and learning system: engineering specification

**Design target, 11 October 2026 · Version 1.** This is an implementation contract for the Listing Tuner service, not a claim that the services or models are deployed. Cars are the first category. A salesperson identifies the stock unit, uploads real photos and phone video, and Crankshaft produces, approves, publishes and measures the listing. The owner-approved [listing accuracy standard](./Listing-Accuracy-Standard.md) applies: dealer statements govern condition/options and listing disclosures; we promote the car's positives, block known false claims, and never digitally remove dents, change vehicle color/parts/condition or replace real media with an AI-created car. Sharpening has no preset strength cap.

## 1. System boundary and deliverables

```text
Dealer DMS/inventory ───► stock snapshots ────┐
Dealer CRM/sales ────────► funnel outcomes ────┤
SignalWire/OpenAI verifier ► call events ──────┤
Salesperson upload ───────► immutable media ───┼─► canonical stock lifecycle
Licensed listing partners ► market snapshots ──┘             │
                                 ┌───────────────────────────┼──────────────────────────┐
                                 ▼                           ▼                          ▼
                         photo worker                 video worker                 copy worker
                                 └──────────────► candidates + hard QA ◄───────────────┘
                                                       │
                                      rank/choose ► dealer approval ► publisher
                                                       │                  │
                                                       └──── live readback ◄┘
                                                                  │
                                             feature/label builder ◄┘
                                                      │
                                            PyTorch training/evaluation
                                                      │
                                          versioned model registry
```

Separate synchronous APIs from asynchronous workers. The upload API returns an asset/batch ID immediately; queues run media analysis, renders, transcriptions, model inference and publishing. PostgreSQL holds transactional state and event receipts. Object storage holds originals and derivatives by tenant/stock lifecycle/content hash. A warehouse or columnar store holds listing-day, call and outcome facts for training. A feature builder creates immutable, point-in-time training snapshots. Model inference cannot write directly to DMS, CRM or a marketplace; only an approved publication service can.

**First release outputs per stock:** approved title/body/feature claims, ordered real-photo gallery and channel-specific derivatives, zero or more clips from supplied footage, approved disclosure payload, destination-specific exports, live publication receipts, and an audit record linking every output to source media/facts and a reviewer. Return an explicit `needs_retake`, `needs_dealer_fact`, `needs_approval` or `publish_failed` state instead of manufacturing missing evidence.

## 2. Canonical identity, events and authority

Use `(tenant_id, stock_id, stock_lifecycle_id)` as the operational key. VIN alone is not a lifecycle key: the same vehicle can be relisted, transferred or sold and later reappear. Record `observed_at` (when the source says it was true), `ingested_at` (when we received it), source ID, version and confidence. A dealer-authorized inventory feed wins for current stock, price, mileage, status and availability. A named dealer attestation or approved feed is sufficient for condition/options; free vPIC is an identity cross-check, not installed-option proof.

Minimum tables or equivalent versioned documents:

| Entity | Required fields and invariant |
|---|---|
| `stock_snapshot` | Tenant/lifecycle, source revision, VIN/stock, vehicle attributes, miles, price/fees, status, dealer-attested facts/disclosures, effective and ingest times. Append changes; never overwrite history. |
| `media_original` | Tenant/lifecycle, object URI, SHA-256, uploader, rights receipt, capture time, EXIF/stream metadata, quarantine state. Original bytes immutable. |
| `media_derivative` | Parent hash, transform/edit-decision-list JSON, software/model versions, destination profile, output hash, reviewer and approval. |
| `listing_version` | Content-addressed source snapshot, ordered media IDs, copy/claim provenance, destination, hard-QA result, model recommendation, dealer approval, publish receipt and live readback. |
| `call_event` | Provider call ID, event ID/type/time, dealer, restricted caller reference, requested stock candidates, verifier model/prompt version, decision evidence, transfer state and CRM receipt. Idempotent by provider event ID. |
| `lead_journey` | Pseudonymous lead key, touchpoints, stock interests, appointment/test drive/offer/sale milestones, match method and confidence. Raw phone number lives in a restricted identity vault. |
| `listing_day` | Listing/version/channel/day, placement/promotion, impressions, detail views, contact starts, qualified calls, appointments, active/sold/other-exit state, censoring mask and market snapshot ID. |
| `experiment_assignment` | Unit, channel, eligible candidate versions, randomization seed/stratum, assigned version, start/stop and exposure. Assignment survives retries. |
| `rights_record` | Asset/source, allowed storage/processing/training/public display, retention/deletion, agreement revision and takedown lineage. No training row without applicable rights. |

Use an outbox/consumer pattern for `stock.changed`, `media.uploaded`, `listing.approved`, `listing.published`, `listing.live_checked`, `call.qualified`, `call.transfer_answered`, `appointment.confirmed`, `vehicle.retail_sold`, `vehicle.other_exit` and `rights.revoked`. Consumers must tolerate duplicate and out-of-order messages. A sold/removed stock event invalidates queued publication and triggers destination reconciliation.

## 3. What the AI verifier and dealer software contribute

The verifier's useful output is a structured *buyer-interest event*, not merely a yes/no lead flag. Extend the existing call decision schema with: `requested_stock_ids[]`, `category/make/model`, `budget_range` if volunteered, desired features, intended use, purchase timeframe, trade-in/financing interest if volunteered, objections (`price`, `mileage`, `condition`, `missing_feature`, `availability`, `other`), appointment intent, qualification state/reasons, whether an agent answered, and explicit unknowns. Store each extracted fact with confidence and an evidence span/time; do not force uncertain speech into a fact. The call service still answers and routes in real time; this logging path must never delay a transfer.

```json
{
  "schema_version": 1,
  "event_type": "call.qualified",
  "tenant_id": "dealer-7",
  "call_id": "sw-call-123",
  "occurred_at": "2026-10-11T16:30:00Z",
  "stock_interests": [{"stock_id": "A104", "confidence": 0.98, "evidence": "caller named stock A104"}],
  "intent": "purchase_in_30_days",
  "desired_features": ["third_row"],
  "objections": [{"code": "price", "confidence": 0.81}],
  "qualification": "qualified",
  "transfer": "agent_answered",
  "listing_touch_id": "touch-opaque-or-null",
  "model_version": "voice-2026-10",
  "policy_version": "dealer-7-v3"
}
```

This record informs two distinct loops. **Per-unit editing:** repeated questions about a genuinely dealer-confirmed third row suggest the copy or photos are hiding that feature; repeated confusion about advertised price suggests the price/fee presentation needs review. **Market learning:** aggregate wanted features and objections by segment/market to help choose which approved facts and views to foreground. Do not publish a feature just because a buyer asked for it. Avoid modeling sensitive personal traits or training directly on raw phone audio by default. Dealer-approved retention and consent controls govern transcripts/recordings; use structured, minimized features for listing models.

The inventory/DMS/CRM adapter contributes stock status, price/mileage changes, days in inventory, ad source where recorded, lead ID, appointment, visit, offer, gross and **confirmed retail sale** when available. Capture wholesale, transfer, auction and unknown removals as separate states. A website disappearance or DMS status change without a known disposition is not a retail-sale label. Different DMS products expose different fields; adapters declare their capabilities and source authority at onboarding.

### Attribution: which listing caused which call?

Attribution is a versioned join, not a guess from the call date. Prefer deterministic evidence: tracked VDP session or click-to-call ID; destination-specific tracking number; CRM lead/source ID; caller explicitly naming the stock; then an authorized privacy-preserving phone/lead match. Record match method and confidence. A caller may mention two vehicles, and one sale may have several touches. Keep those as multi-stock journeys rather than crediting every listing with a full sale. For the primary supervised label, require a high-confidence stock and a listing version known to be live before the touch. Use lower-confidence calls only in aggregate analyses or sensitivity tests. Keep a channel-level `unattributed_call` bucket; forcing all calls onto a listing would corrupt training data.

## 4. Exact photo-processing pipeline

1. **Ingest and quarantine:** verify file type/size, compute SHA-256 and perceptual hash, extract EXIF orientation, dimensions and color profile, preserve original bytes, remove public GPS metadata only from derivatives. Match the batch to a stock lifecycle using uploader selection plus visible identity checks; send mixed-car or ambiguous sets to review.
2. **Measure candidate quality:** compute blur and motion smear, clipped highlights/shadows, mean/local exposure, glare, horizon tilt, subject bounding box and occupancy, occlusion, duplicate similarity and privacy flags. Classify view type (exterior angle, side, wheel, cabin, seating, controls, odometer, cargo, dealer-requested condition view). Calibrate cutoffs by camera/category; an odometer shot needs readability, while a hero needs framing.
3. **Generate bounded, reproducible edits:** EXIF rotation, optional measured lens correction, straighten, candidate crop rectangles at channel aspect ratios, exposure/white-balance/contrast adjustments, denoise, unrestricted editorial sharpening, resize/compress and privacy masking. Do **not** use generative fill or an AI-created vehicle/background. Every candidate is a transform graph over the original and has a parameter JSON plus parent hash. Preserve true paint/upholstery color and visible condition; do not digitally erase dents, damage, warning lights, badges or parts.
4. **Score the candidates:** hard gate wrong stock, unusable resolution, missing required dealer view, and edits that alter the car. Within each view class, the photo ranker scores useful composition and clarity. Score the *set* for angle coverage, distinctness and mobile first-screen impact. Greedy selection or a small integer optimizer can maximize `Σ image_score + coverage_bonus − duplicate_penalty` with explicit constraints: one hero exterior, required views, destination count and ratio limits. The model does not decide disclosure policy.
5. **Human/dealer review:** show original beside proposed export at full size, the proposed gallery order, missing-shot requests and relevant dealer disclosure instructions. Save reviewer changes as future preference labels. Export clean masters and destination sizes only after approval; compare live hero/order with the approved version.

`photo_edit_recipe` should include `{original_sha256, pipeline_version, color_profile, rotate_deg, crop_xywh, exposure_ev, white_balance, denoise_params, sharpen_params, resize, privacy_masks, output_sha256}`. Make renders deterministic from this recipe. A failed or canceled render cannot silently fall back to a synthetic image. The first release can use ordinary image-processing libraries plus human review; learned crop/edit-parameter prediction follows only after labels exist.

## 5. Exact phone-video clipping pipeline

1. **Ingest/probe:** save original and rights receipt; run `ffprobe` to capture codec, frame rate, resolution, rotation, duration, streams and corruption. Normalize timestamps and orientation in an analysis proxy; keep original media unchanged. [FFprobe documentation](https://ffmpeg.org/ffprobe.html).
2. **Create a timecoded scene map:** voice-activity detection and timestamped ASR; shot-boundary detection; representative frames every N seconds and at boundaries; OCR only as a prompt for human verification; quality curves for focus, exposure, shake, vehicle occupancy and audio level. Link scenes to exterior, interior, controls, cargo and dealer-attested feature tags. Store time ranges in milliseconds against the original.
3. **Generate candidates:** form intervals around coherent visual actions and complete spoken thoughts. Reject wrong-car frames, known false narration, severe blur, unsafe scenes, rights conflicts or intervals too short to understand. Keep overlapping candidates for ranking; do not concatenate arbitrary words into a new sentence.
4. **Rank and assemble:** a rules baseline scores quality, distinctness and feature usefulness. Optionally send compact scene metadata, checked transcript spans and approved facts to Jev for candidate ranking; benchmark Jev against editor selections and the baseline. Jev is advisory and does not edit footage. Solve clip assembly under a duration budget, no-overlap rule, view-diversity target and channel goal. A usable shoot can yield an overview, feature-specific clips and a horizontal recap; do not enforce a quota on weak footage. [HE Jev video example](https://www.hejev.com/ai-jev/).
5. **Produce an edit decision list:** `[{source_sha256, in_ms, out_ms, crop_track, stabilization, exposure, audio_gain, caption_spans}]` plus aspect/codec/bitrate profile. A subject tracker proposes 9:16 crops and checks that the intended car/detail remains visible; use padding or a horizontal output when cropping would misrepresent or obscure it. FFmpeg makes the cuts, reframes, stabilizes, normalizes audio and encodes. [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html).
6. **Validate the final render:** check decoder errors, length/aspect/audio, caption-to-speech alignment, stock identity, privacy and platform requirements. An editor watches the entire export with sound and compares sensitive cuts with source. Dealer approves when configured; publisher checks each live destination. Preserve render logs and edit decision list. Ask for a precise retake if no useful interval survives.

## 6. Model plan: separate quality, response and sale outcomes

The model must rank *editable presentation choices for the same or comparable stock*, while controlling for car desirability, dealer, price, promotion, market and channel. A high-priced car that sells slowly is not automatically a poor listing. The model should not learn that a large dealer's ad budget is “good photography.”

### 6.1 Photo usefulness model — starter exists

The repository's [`ml/photo_ranker.py`](./ml/photo_ranker.py) uses a pretrained-capable MobileNetV3-Small encoder, eight measured image features, a view-classification head and a scalar usefulness head. The [`ml/train_photo_ranker.py`](./ml/train_photo_ranker.py) script takes dealer-authorized pairs **within the same view type**, where editors choose A or B, and minimizes a pairwise logistic loss `softplus(-preference × (score_A − score_B))` plus view-class cross entropy. Start with a rules baseline and measure held-out pair accuracy, view accuracy, calibration by camera/dealer and editor override rate. The code is untrained; `--pretrained` fetches public image weights, not automotive preferences. [Torchvision MobileNetV3](https://docs.pytorch.org/vision/stable/_modules/torchvision/models/mobilenetv3.html).

Next add a **set-level gallery model**: encode each selected photo, its view type and order; use attention or a small permutation-aware encoder to estimate coverage, redundancy and first-screen quality. Train first against editor judgments of complete galleries, then against qualified response only when there is enough controlled exposure data. A simple diversity optimizer may outperform this network early; keep it as the baseline.

### 6.2 Video and copy representations

For video, begin with deterministic scene metrics and optional Jev rankings. Once editors have labeled thousands of candidate pairs, train a PyTorch interval ranker with pooled frame embeddings, motion/stability, scene class, checked transcript embedding and audio metrics. Its training target is editor acceptance/usefulness, not predicted sales from a tiny set of videos. Hold out whole vehicle videos and dealers.

For copy, generate candidates only from dealer-authorized claim records. Encode the approved text and structured claim features with a pretrained text encoder; do not train a free-form language model from scratch on scraped ads. A claim-source validator runs before any performance model. The response model may learn which *valid* facts and ordering work in a market, but it cannot invent options or suppress dealer-directed disclosures.

### 6.3 Exposure-aware funnel and sale model

Build one row per `stock_lifecycle × listing_version × channel × day`, joined point-in-time to a local market snapshot. Numeric inputs: relative price and price changes, age/miles, inventory age, local supply, placement, paid spend, season and approved condition/category fields. Categorical embeddings: vehicle segment, dealer/site, geography and channel. Presentation inputs: photo-set embedding/order, text embedding/specificity, clip presence/quality and disclosure completeness. Missing outcome fields have explicit masks; zero is not interchangeable with “unavailable.”

Train separate, interpretable heads for the funnel: eligible detail-view session → attributable contact; attributable answered call → qualified call; qualified call → confirmed appointment. Use binomial/BCE style likelihoods with exposure denominators and masks. For confirmed sale timing, use a daily competing-risk head `active / retail_sale / other_confirmed_exit`; omit unobserved days after the last trusted status and do not label unknown delists as sales. The current [`ml/listing_demand.py`](./ml/listing_demand.py) is only an untrained skeleton for that last head. PyTorch provides stable binary and multiclass losses; the real work is clean event joins and labels. [PyTorch BCEWithLogitsLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html), [CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html).

The primary ranking quantity is **expected qualified appointments per 1,000 eligible VDP sessions** for a specific car/market/channel, with uncertainty. An optional downstream term uses confirmed retail-sale probability and dealer-provided gross/holding economics, but only after those outcomes are reliable. Do not optimize raw call volume: the verifier lets us distinguish qualified buyers from wrong-number, service, spam or unqualified inquiries. Report each funnel stage separately so the model cannot hide a drop in call quality behind more clicks.

### 6.4 Candidate selection and uncertainty

Generate a small, auditable candidate set: several real-photo heroes/orders/crops, valid headline/body arrangements and available clips. Apply hard gates **before** scoring: authorized media, correct stock, current price/status, no known false claim or altered vehicle, required dealer listing instructions, destination format. Score only survivors. Choose the best expected outcome subject to a minimum-confidence rule; when predicted differences are within uncertainty, prefer the simpler or cheaper version and collect more evidence. Log all candidates and scores, not only the winner, for later off-policy analysis. Never let the model directly change price or legal/disclosure policy.

## 7. Training data, leakage prevention and evaluation

**Data acquisition:** first collect dealer-authorized originals, editor preferences and CRM/DMS outcomes. Under signed partner agreements, ingest listing text/media/lifecycle snapshots and any exposure/outcome data the partner licenses. The optimistic target of 100,000–250,000 listing lifecycles is procurement scale, not existing access. Without exposure and verified outcomes, partner data can train representations and editorial labels; it cannot prove which listings convert. The current 40-listing gallery is a diagnostic sample only.

**Point-in-time features:** a training example for October 11 can use only price, market, stock and media known by October 11. Never join in a later sale status, edited price, final listing text or future view counts as an input. Split whole stock lifecycles and dealers, then test on later months and unseen partner sites. Deduplicate the same vehicle/media across sites before splitting. Fit categorical vocabularies and normalization on the training partition only. Keep source-rights IDs on every row and derived embedding.

**Offline gates:** pairwise photo/video agreement with independent editors; view/scene classification; appointment-rate ranking and calibration by dealer/market/segment; sale-hazard calibration; missing-data robustness; wrong-stock/known-false publication rate; publication latency and editor minutes. Compare against simple rules and tabular models. A network ships only if it improves relevant holdouts and meets the hard media/claim gates.

**Online proof:** on dealer-owned pages or authorized channels, randomize eligible stock/listing versions within price/vehicle/market strata and hold the assignment stable for a defined window. Test one intervention at a time (hero, photo order, copy or clip); log impressions, position and paid spend. Primary metric: qualified appointments per eligible VDP session, with verifier outcomes and CRM confirmations. Track contact rate, qualification rate, transfer-answer rate, dealer-confirmed sale and time-to-sale as secondary measures. Where randomization is impossible, show matched observational comparisons with uncertainty; do not describe them as causal lift. Stop a variant immediately for a factual/media error.

**Verifier feedback audit:** periodically sample call classifications against dealer/agent dispositions. If the verifier changes prompt/model or dealer routing policy, version the label source and check for drift before using those calls in retraining. A misrouted but interested buyer should not become a negative listing label. Appointment no-shows and CRM omissions need separate states rather than silently becoming failures.

## 8. Service/API contracts and build order

Minimum internal interfaces (all tenant-scoped, versioned and idempotent): `POST /media/batches`, `GET /media/{id}/analysis`, `POST /media/{id}/render`, `POST /listings/{stock}/candidates`, `POST /listings/{version}/approve`, `POST /listings/{version}/publish`, `POST /events/verifier`, `POST /events/inventory`, `POST /events/crm`, `GET /stock/{id}/funnel`, and `POST /models/{version}/score`. Provider-specific adapters translate DMS/CRM feeds and receipts to canonical events; the ML services consume canonical data only. Authentication, webhook signatures, tenant isolation, backpressure and retry/dead-letter queues are required. A caller's speech cannot write listing claims or routing policy.

Implementation sequence with release evidence:

1. **Data foundation:** one dealer inventory read adapter, stock lifecycle/event store, upload API/object storage, verifier event schema, CRM receipt and deterministic lead/stock join. Demonstrate one stock, one real upload, one qualified call and one confirmed CRM appointment joined without cross-tenant data.
2. **Rules-first media:** view/quality detection, deterministic photo recipes, video scene map/EDL/FFmpeg renderer, operator review UI, dealer approval and one authorized publishing adapter. Demonstrate original-to-live provenance, correct car/color/condition and a sold-stock withdrawal.
3. **First PyTorch photo model:** obtain licensed/dealer photo-pair labels, train the existing ranker, compare with rules on unseen dealers, deploy advisory scoring behind versioned inference. Measure editor override and time saved; no automatic publication yet.
4. **Feedback warehouse and outcome baseline:** daily listing exposure and inventory/CRM/verifier joins, confirmed sale vs other exit, source-quality audit, simple market-adjusted tabular baseline. Produce a dealer-level funnel report before training a response network.
5. **Outcome model and experiments:** train/calibrate exposure-aware heads, add bounded candidate scoring, run authorized randomized tests, then expand channel/dealer coverage. Add Jev or a learned video ranker only if a controlled benchmark shows better accepted clips or lower editor time without more errors.

**Current repository status:** `ml/` contains a free vPIC identity adapter, untrained photo-ranking model/trainer and an untrained daily demand-model skeleton. There is no media worker, event warehouse, trained model, live DMS/CRM integration or verified conversion lift. This document defines the work the engineering team would implement and the evidence needed before declaring the system automatic.
