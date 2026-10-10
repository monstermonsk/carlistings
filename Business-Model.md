# Crankshaft commercial model and unit economics

**Proposed launch pricing, 10 October 2026.** Crankshaft is the company and Listing Tuner is its managed listing service. The dealer pays one monthly plan fee for listing work and included AI call handling. **There are no separate minute, decision or token charges.** A dealer needing more recurring capacity upgrades its plan.

| Monthly plan | Launch | Growth | Scale |
|---|---:|---:|---:|
| Established monthly fee | $795 | $1,295 | $1,995 |
| Active listings covered | 30 | 60 | 100 |
| New/rebuilt listings per month | 20 | 40 | 70 |
| Clips from client footage per month | 10 | 25 | 50 |
| Included AI verifier minutes per month | **750** | **1,500** | **2,500** |
| Minutes per active listing | 25 | 25 | 25 |

The minutes scale directly with active listings: **30 / 60 / 100 × 25 minutes**. This is a generous plan ceiling, not a claim that each listing will produce 25 minutes of calls. For initial demand sizing, assume **1.5 in-scope inbound sales calls per active listing per month × 3 AI minutes per call**. That implies about **135 / 270 / 450** likely AI minutes; the plan ceilings provide room for a much busier dealer. Listing grades describe listing quality and do not themselves predict phone volume. Measure per-listing views, calls, AI duration and qualified outcomes during the pilot, then replace this sizing assumption. Whole-rooftop benchmarks include other departments and cannot be copied directly to a listing-sourced sales line. [Foureyes 2026 dealer benchmarks](https://www.foureyes.io/blog/2026-automotive-dealer-benchmarks-report); [CallRevu call analysis](https://www.callrevu.com/2021/01/27/understanding-the-roi-of-your-inbound-calls/).

An **AI verifier minute** is connected time while the verifier handles a call, ending when it releases the caller to a salesperson or fallback. Aggregate connected seconds per dealer over the month and round once to whole minutes for the dashboard. The transfer conversation after AI release does not consume included AI minutes; Crankshaft still bears applicable carrier cost. The dealer sees usage at 70% and 90% and an upgrade proposal before reaching the plan ceiling. At the ceiling without an upgrade, new callers follow the agreed human or callback path; they are never silently dropped or billed an overage. International, premium-rate and outbound campaign traffic need a separately agreed plan scope.

**Pilot:** $495 for ten vehicles, two sample clips from client footage, read-only integration assessment and limited test calls, credited toward month one if a plan begins within 30 days. Nonstandard vendor certification or connector work needs a separate setup quote.

## Supplier costs inside the plan

SignalWire lists US local inbound PSTN at **$0.00660/minute** and outbound at **$0.00800/minute**. A simultaneous inbound and outbound PSTN bridge illustrates **$0.01460 per minute** in transport, before number fees, features, different leg durations and rounding. The model uses **$0.05 of telecom cost per AI minute** to allow for the transfer leg after AI release; this is an internal planning allowance, not a customer price or a carrier quote. SignalWire's separate AI Agent product is excluded because the verifier uses OpenAI voice. [SignalWire pricing](https://signalwire.com/pricing).

The owner reports about **30,000 total measured OpenAI tokens per verifier decision**. Modality and input/output split remain unconfirmed. At an illustrative 24,000 input / 6,000 output split, `gpt-realtime-2.1` would cost **$1.152 if all were audio tokens**, **$0.24 if all were text tokens**; `gpt-realtime-2.1-mini` would be about **$0.36 for the all-audio case**. Actual mixed and cached usage may differ. The workbook conservatively uses the full audio model and **one decision per three-minute call**, equivalent to **$0.384 token cost per AI minute**, plus the $0.05 telecom allowance. A second decision per call would raise internal token cost to $0.768 per AI minute. None of these supplier costs appears as a separate dealer invoice item. [OpenAI pricing](https://developers.openai.com/api/docs/pricing).

| Full plan use, one decision per 3-minute call | Launch | Growth | Scale |
|---|---:|---:|---:|
| Monthly plan fee | $795 | $1,295 | $1,995 |
| Listing labor + video + tools/QA allowance | $455 | $845 | $1,485 |
| Internal voice cost at $0.434/AI minute | $326 | $651 | $1,085 |
| Illustrative contribution | **$15** | **($201)** | **($575)** |
| Contribution margin | **2%** | **(16%)** | **(29%)** |

These are full-allowance stress illustrations, before fixed operating costs, acquisition, setup, taxes and payment fees. Restoring the established prices while retaining 750/1,500/2,500 included minutes creates a **material margin risk** at full use. Even at one full-audio decision per three-minute call, Growth and Scale are negative on direct cost. At two decisions, Scale's direct contribution is about **($1,535)**. Actual token modality, decision count and minute utilization are pilot gates. Keep the established price on the materials as requested, but do not make an unconditional full-use margin claim; optimize the verifier or revisit scope and economics before signing long-term capacity commitments.

## Market and forecast

AI voice competitors publish much lower stand-alone usage prices, but they do not include managed listings and clip production: [AutoJoy](https://www.autojoy.ai/), [iCarManager](https://icarmanager.com/), and [SpaceStep](https://www.spacestep.ca/voice-ai-agent-for-car-dealerships). Crankshaft's monthly fees are proposed packages, not surveyed transaction prices. Verify competitors and actual dealer willingness to pay in sales calls.

The [24-month workbook](./financials/Crankshaft-24-Month-Model.xlsx) includes **no minute overage, token charge or plan-upgrade revenue**. Its base case assumes **18% of included AI minutes are used** at the one-decision, full-audio cost case and calculates listing/media costs separately. Change the utilization assumption to 100% to test the full allowance. Review the [model guide](./financials/Model-Guide.md) before using its cash forecast in financing decisions.
