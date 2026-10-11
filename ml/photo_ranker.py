"""Starter PyTorch model for dealer-authorized, pairwise photo ranking."""

from __future__ import annotations

import torch
from torch import nn
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

VIEW_NAMES = (
    "front_left", "rear_right", "front", "rear", "left_side", "right_side",
    "wheel", "cockpit", "controls", "front_seats", "rear_seats",
    "odometer", "cargo", "defect", "other",
)
METRIC_NAMES = (
    "blur", "brightness", "highlights_clipped", "shadows_clipped",
    "subject_coverage", "horizon_tilt", "glare", "occlusion",
)


class PhotoRanker(nn.Module):
    """Predict relative usefulness within a view class and classify the view.

    Scores are advisory. Wrong-stock, disclosure and truthfulness gates live in
    deterministic policy code outside this model.
    """

    def __init__(self, pretrained: bool = False) -> None:
        super().__init__()
        weights = MobileNet_V3_Small_Weights.DEFAULT if pretrained else None
        self.encoder = mobilenet_v3_small(weights=weights)
        feature_dim = self.encoder.classifier[0].in_features
        self.encoder.classifier = nn.Identity()
        self.fusion = nn.Sequential(
            nn.Linear(feature_dim + len(METRIC_NAMES), 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
        )
        self.usefulness = nn.Linear(128, 1)
        self.view = nn.Linear(128, len(VIEW_NAMES))

    def forward(self, image: torch.Tensor, metrics: torch.Tensor) -> dict[str, torch.Tensor]:
        if metrics.ndim != 2 or metrics.shape[1] != len(METRIC_NAMES):
            raise ValueError(f"metrics must have shape [batch, {len(METRIC_NAMES)}]")
        features = self.encoder(image)
        fused = self.fusion(torch.cat((features, metrics), dim=1))
        return {"score": self.usefulness(fused).squeeze(1), "view_logits": self.view(fused)}
