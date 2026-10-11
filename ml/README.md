# Developer starter: vehicle identity and photo ranking

This is **starter code**, not a deployed service or trained model. `vin_lookup.py` calls the free [NHTSA vPIC API](https://vpic.nhtsa.dot.gov/api/) and deliberately returns `installed_options_verified: false`. The business workflow must reconcile its identity candidates with dealer records and a separate build-data or option-proof source.

`photo_ranker.py` defines a MobileNetV3-Small model with a pairwise usefulness score and a view-class head. `train_photo_ranker.py` trains only on dealer-authorized, labeled pairs. Install PyTorch, matching torchvision and Pillow using the [official PyTorch selector](https://pytorch.org/get-started/locally/) for the target CPU/GPU. Then, from the repository root, run:

`listing_demand.py` is an untrained second-stage model for daily sale/other-exit probabilities from licensed lifecycle data. It keeps confirmed sales separate from other removals and masks unknown or unobserved days. Build a simple tabular survival baseline and validate by dealer, partner site and future month before choosing this neural model for production.

```bash
python -m ml.train_photo_ranker path/to/manifest.jsonl path/to/photo-ranker.pt --pretrained
```

The `--pretrained` flag downloads public ImageNet weights; without it, weights start randomly and need much more licensed training data. No model weights or training media are bundled here.

Each JSONL row contains `split` (`train` or `val`), `dealer_id`, `stock_lifecycle`, `view`, `preferred` (`1` for A, `-1` for B), and `a`/`b` objects with an image path relative to the manifest and eight normalized metrics. Example (one line; add many independent stock groups before training):

```json
{"split":"train","dealer_id":"dealer-1","stock_lifecycle":"stock-81-v1","view":"front_left","preferred":1,"a":{"image":"images/a.jpg","metrics":{"blur":0.8,"brightness":0.6,"highlights_clipped":0.0,"shadows_clipped":0.1,"subject_coverage":0.7,"horizon_tilt":0.1,"glare":0.0,"occlusion":0.0}},"b":{"image":"images/b.jpg","metrics":{"blur":0.2,"brightness":0.3,"highlights_clipped":0.1,"shadows_clipped":0.2,"subject_coverage":0.4,"horizon_tilt":0.3,"glare":0.2,"occlusion":0.0}}}
```

Metric scaling and annotation instructions must be fixed before labeling. A's and B's view label should match. Hold out whole dealers, ensure each stock lifecycle appears in only one split, and run a later time holdout. The loader rejects dealer or lifecycle overlap. This code does not implement stock matching, defect preservation, cropping, video editing, Jev calls or marketplace publishing; those are separate audited services in the [operating plan](../Salesperson-to-Listing-Operating-Plan.md).
