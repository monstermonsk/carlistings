"""Untrained daily listing-demand model for licensed lifecycle and outcome data."""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F

# Daily outcome labels: a confirmed sale is distinct from withdrawal/transfer.
ACTIVE, CONFIRMED_SALE, OTHER_CONFIRMED_EXIT = 0, 1, 2


class ListingDemandModel(nn.Module):
    """Estimate daily competing outcomes conditional on being active today.

    Numeric inputs should include listing age, relative price, miles, vehicle age,
    local supply, season, and observed placement. Image/text embeddings come from
    separately trained encoders. Category IDs must be fitted on training data only.
    """

    def __init__(
        self,
        numeric_dim: int,
        image_dim: int,
        text_dim: int,
        segments: int,
        markets: int,
        channels: int,
    ) -> None:
        super().__init__()
        self.segment = nn.Embedding(segments, 16)
        self.market = nn.Embedding(markets, 16)
        self.channel = nn.Embedding(channels, 8)
        width = numeric_dim + image_dim + text_dim + 40
        self.head = nn.Sequential(
            nn.Linear(width, 128), nn.ReLU(), nn.Dropout(0.2),
            nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 3),
        )

    def forward(
        self,
        numeric: torch.Tensor,
        image_embedding: torch.Tensor,
        text_embedding: torch.Tensor,
        segment_id: torch.Tensor,
        market_id: torch.Tensor,
        channel_id: torch.Tensor,
    ) -> torch.Tensor:
        features = torch.cat((
            numeric, image_embedding, text_embedding,
            self.segment(segment_id), self.market(market_id),
            self.channel(channel_id),
        ), dim=1)
        return self.head(features)


def observed_daily_loss(
    logits: torch.Tensor,
    outcome: torch.Tensor,
    observed: torch.Tensor,
) -> torch.Tensor:
    """Cross-entropy for observed active days; omit days after censoring.

    `outcome` is 0 while confirmed active, 1 on a confirmed sale day, 2 on
    another confirmed exit day. Unknown disappearance is never relabeled sale.
    `observed` is false for days without a trusted status or after last sighting.
    """
    mask = observed.bool()
    if not torch.any(mask):
        raise ValueError("Batch contains no observed listing-days")
    return F.cross_entropy(logits[mask], outcome[mask].long())
