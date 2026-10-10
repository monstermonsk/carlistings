# Sources, scope and assumptions

Research checked 10 October 2026. Vendor prices and API access can change; recheck before contract or implementation. Links point to primary vendor documentation where available. Proposed Crankshaft prices and margins are our model, not published vendor facts.

## Brand and workflows

- [Crankshaft live site](https://crankshaft.ai/): observed company name, visual mark, graphite/amber visual language and current verified-call positioning. The new local preview does not change the live site.
- [HE Jev video use case](https://www.hejev.com/ai-jev/): describes transcribing candidate footage and Jev ranking moments; editing occurs in other software.
- [HE Jev API note](https://www.hejev.com/jev-api/) and [TypeSafe quickstart](https://docs.typesafe.ai/introduction/quickstart): actual typed decision API and `jev-latest` example. Confirm current API product, terms, limits and ability to score structured candidate metadata during implementation.

## Voice and dealer integrations

- [OpenAI Realtime SIP](https://developers.openai.com/api/docs/guides/voice-sip?voice-api=realtime), [Realtime conversations](https://developers.openai.com/api/docs/guides/realtime-conversations), [voice latency/cost](https://developers.openai.com/api/docs/guides/voice-latency-cost) and [pricing](https://developers.openai.com/api/docs/pricing): architecture and current model rates. The owner reports 30k **total measured tokens per decision**; the modality split remains to be verified and is not a documented OpenAI norm.
- [SignalWire pricing](https://signalwire.com/pricing), [voice calls](https://signalwire.com/docs/platform/voice/make-and-receive-calls), [call transfer](https://signalwire.com/docs/server-sdks/guides/call-transfer): published transport rate examples and technical route options. Actual invoice depends on number, geography, call legs, recording and selected products.
- [Fortellis developer network](https://docs.fortellis.io/docs/general/overview/getting-started), [API directory](https://docs.fortellis.io/docs/general/api-directory-marketplace/api-directory/), [Merchandisable Vehicles API](https://community.fortellis.io/merchandisable-vehicles-api/merchandisable-vehicles/apis): examples of dealership API paths, not a guarantee that a specific dealer grants Crankshaft access.
- [ADF 1.0 lead format](https://adfxml.info/adf_spec.pdf): standard XML lead schema. CRM-specific mapping and acknowledgement still require testing.

## Commercial comparison

- [AutoJoy](https://www.autojoy.ai/), [iCarManager](https://icarmanager.com/), [SpaceStep](https://www.spacestep.ca/voice-ai-agent-for-car-dealerships): publicly stated voice pricing used for range checking, not like-for-like substitutes for a combined managed listing and verifier service.
- [Foureyes 2026 dealer benchmarks](https://www.foureyes.io/blog/2026-automotive-dealer-benchmarks-report) and [CallRevu inbound call discussion](https://www.callrevu.com/2021/01/27/understanding-the-roi-of-your-inbound-calls/): dealer call context. Neither supplies a validated calls-per-active-listing rate for this service. The planning assumption of 1.5 in-scope calls per listing per month and three AI minutes per call must be replaced with pilot observations.

## 40 sample listing observations

All 40 sample records were observed on [Autotrader](https://www.autotrader.com/cars-for-sale/used-cars) in the Southwest Florida search context during this research session. Each record has its exact listing URL in the gallery. The local source photo is a marketplace thumbnail and may differ from the full image set. We captured only the visible card title, advertised price, seller when shown, and one thumbnail. We **did not verify each full listing description, vehicle history, VIN, equipment, condition or fee schedule**. Accordingly grades are **card-level presentation grades**, and rewritten copy is a proposal that says only what the observed card supports. Specific suggestions tell an editor what to verify or photograph, not facts asserted about the vehicle. Live inventory and prices can change after capture. No video was downloaded or edited.

The sample photo files are for the owner's local review. A dealer must supply originals and grant media rights before any Crankshaft production use or public redistribution. The gallery's browser treatment is reversible framing/light adjustment, not alteration of the vehicle itself.
