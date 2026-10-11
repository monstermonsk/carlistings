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

## Vehicle identity, option data, media and model training

- [NHTSA vPIC API](https://vpic.nhtsa.dot.gov/api/): free VIN decoding, batch and standalone database; manufacturer-submitted VIN structure data and rate controls. It does not establish every installed option.
- [Wenmar Open API](https://open.wenmarpro.com/docs): no-key free VIN/catalog API with published limits; its stated data source is vPIC, so it is not independent build proof.
- [EPA FuelEconomy.gov web services](https://www.fueleconomy.gov/feg/ws/index.shtml): configuration fuel-economy data, not unit-specific VIN options.
- [DataOne option-level VIN API](https://www.dataonesoftware.com/web-services-vin-decoder-api), [Auto.dev OEM Build Data](https://docs.auto.dev/v2/products/oem-build-data): candidate commercial sources for installed-option/build details. Access, coverage and pricing need a dealer/provider pilot.
- [Torchvision MobileNetV3](https://docs.pytorch.org/vision/main/models/generated/torchvision.models.mobilenet_v3_small.html), [PyTorch transfer learning](https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial): basis for the starter photo ranker; no training claim is made for the code in this package.
- [FFprobe](https://ffmpeg.org/ffprobe.html), [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html): media inspection and rendering components, subject to footage quality and review.
- [Born et al., Price Management in the Used-Car Market](https://www.econstor.eu/bitstream/10419/230775/1/irtg1792dp2018-065.pdf): published survival-analysis approach for used-car demand and price response; Crankshaft's cohort controls and success metrics still need its own data validation.

The new operating plan assumes the founder can negotiate site-owner revenue-share agreements that explicitly grant bulk download/permitted crawling and model-training rights. Dataset targets and outcome-data access are plans, not current assets. The 40 observed marketplace cards are not used as training media in the public repository.

## Commercial comparison

- [AutoJoy](https://www.autojoy.ai/), [iCarManager](https://icarmanager.com/), [SpaceStep](https://www.spacestep.ca/voice-ai-agent-for-car-dealerships): publicly stated voice pricing used for range checking, not like-for-like substitutes for a combined managed listing and verifier service.
- [Foureyes 2026 dealer benchmarks](https://www.foureyes.io/blog/2026-automotive-dealer-benchmarks-report) and [CallRevu inbound call discussion](https://www.callrevu.com/2021/01/27/understanding-the-roi-of-your-inbound-calls/): dealer call context. Neither supplies a validated calls-per-active-listing rate for this service. The planning assumption of 1.5 in-scope calls per listing per month and three AI minutes per call must be replaced with pilot observations.

## 40 sample listing observations

All 40 sample records were observed on [Autotrader](https://www.autotrader.com/cars-for-sale/used-cars) in the Southwest Florida search context during this research session. Each record has its exact listing URL in the gallery. The local source photo is a marketplace thumbnail and may differ from the full image set. We captured only the visible card title, advertised price, seller when shown, and one thumbnail. We **did not verify each full listing description, vehicle history, VIN, equipment, condition or fee schedule**. Accordingly grades are **card-level presentation grades**, and rewritten copy is a proposal that says only what the observed card supports. Specific suggestions tell an editor what to verify or photograph, not facts asserted about the vehicle. Live inventory and prices can change after capture. No video was downloaded or edited.

The sample photo files are for the owner's local review. A dealer must supply originals and grant media rights before any Crankshaft production use or public redistribution. The gallery's browser treatment is reversible framing/light adjustment, not alteration of the vehicle itself.
