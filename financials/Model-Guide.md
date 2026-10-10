# Crankshaft 24-month model guide

Open [Crankshaft-24-Month-Model.xlsx](./Crankshaft-24-Month-Model.xlsx). `Summary` shows two annual results, `Assumptions` contains editable yellow cells, and `Forecast` calculates October 2026 through September 2028. This is a planning model, not a customer commitment or financing plan.

## Established prices and minutes

The monthly prices are restored to **$795 / $1,295 / $1,995** for 30 / 60 / 100 active listings. Proposed included AI verifier minutes are **750 / 1,500 / 2,500**, the latter following the owner's specified top-plan allowance. No minute, token, decision or upgrade revenue is forecast. The dealer would see one plan fee and upgrade plans if ongoing call volume grows.

The **base case uses 18% of included AI minutes**: an explicit assumption of 1.5 in-scope calls per active listing per month × three AI minutes per call, or 135 / 270 / 450 minutes. Listing grades do not establish call traffic. Replace this assumption with tracked pilot calls. Setting `Assumptions!B14` to **100%** tests full use of every included minute; at the established prices, that creates negative direct margin overall. It must be treated as a material commercial risk before the 2,500-minute allowance is promised to dealers.

The owner reported about **30,000 total measured OpenAI tokens per verifier decision**. The workbook uses a conservative, unverified 24,000 audio input / 6,000 audio output split on `gpt-realtime-2.1`, one decision per three-minute AI call, and $0.05 SignalWire transport allowance per AI minute including a transfer-leg reserve. It bundles these costs into the plan. More decisions or heavier audio output increase internal costs; they are never billed as a separate token item to the dealer.

## Base forecast

The plan mix is 50% Launch, 35% Growth and 15% Scale. New accounts are 1/month in months 1–3, 2/month in months 4–12, and 3/month thereafter, with 2% monthly opening-account churn. New accounts contribute half a month of fees in their first month. Fixed operating cost is $8,000/month and acquisition cost $500 per new account. The $50,000 opening cash input is illustrative and is not committed funding.

| Result | Year 1 | Year 2 |
|---|---:|---:|
| Revenue | $121,555 | $465,536 |
| Gross profit | $32,175 | $123,224 |
| Operating profit | **($74,325)** | **$9,224** |
| Ending accounts, expected value | 19.1 | 47.3 |
| Ending cash, simplified | **($24,325)** | **($15,101)** |

Fractional accounts represent forecast expectations. Cash assumes immediate collections and equal expense/cash timing; it excludes receivables, taxes, debt, setup costs, capital spending and working capital. The negative cash result means additional funding, lower fixed costs, faster growth or revised scope is needed under this scenario. No plan upgrades, media automation savings or conversion gains are assumed.

To test voice risk, edit `Assumptions!B14` for utilization, `B15` for decisions per call, `B16` for AI call length, `B17:B20` for token inputs and rates, and `B21` for the telecom allowance. `Forecast` row 13 is an upgrade signal when minutes exceed the plan; row 14 remains zero because Crankshaft does not bill usage overages. Recheck measured provider invoices and editor time before using the model in a quote or fundraising presentation.
