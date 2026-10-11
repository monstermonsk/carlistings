"""Train on licensed photo pairs: python -m ml.train_photo_ranker manifest.jsonl output.pt"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import torch
from PIL import Image
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from .photo_ranker import METRIC_NAMES, VIEW_NAMES, PhotoRanker

TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
])


class PairDataset(Dataset):
    def __init__(self, rows: list[dict], root: Path) -> None:
        self.rows, self.root = rows, root.resolve()

    def __len__(self) -> int:
        return len(self.rows)

    def _image(self, relpath: str) -> torch.Tensor:
        path = (self.root / relpath).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("Image path escapes the dataset root")
        with Image.open(path) as image:
            return TRANSFORM(image.convert("RGB"))

    def __getitem__(self, index: int):
        row = self.rows[index]
        a, b = row["a"], row["b"]
        view = VIEW_NAMES.index(row["view"])
        return (
            self._image(a["image"]),
            torch.tensor([float(a["metrics"][k]) for k in METRIC_NAMES]),
            self._image(b["image"]),
            torch.tensor([float(b["metrics"][k]) for k in METRIC_NAMES]),
            torch.tensor(float(row["preferred"])),
            torch.tensor(view),
        )


def load_rows(manifest: Path) -> tuple[list[dict], list[dict]]:
    rows = [json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()]
    train = [r for r in rows if r.get("split") == "train"]
    val = [r for r in rows if r.get("split") == "val"]
    if not train or not val:
        raise ValueError("Manifest needs separate nonempty train and val splits")
    train_groups = {(r["dealer_id"], r["stock_lifecycle"]) for r in train}
    val_groups = {(r["dealer_id"], r["stock_lifecycle"]) for r in val}
    if train_groups & val_groups:
        raise ValueError("The same stock lifecycle appears in train and val")
    if {r["dealer_id"] for r in train} & {r["dealer_id"] for r in val}:
        raise ValueError("A dealer appears in both train and val; hold out whole dealers")
    for row in rows:
        if row["preferred"] not in (-1, 1) or row["view"] not in VIEW_NAMES:
            raise ValueError("Invalid preference or view label")
    return train, val


def run_epoch(model, loader, optimizer, device):
    training = optimizer is not None
    model.train(training)
    total, correct, count = 0.0, 0, 0
    for image_a, metrics_a, image_b, metrics_b, preferred, view in loader:
        image_a, metrics_a = image_a.to(device), metrics_a.to(device)
        image_b, metrics_b = image_b.to(device), metrics_b.to(device)
        preferred, view = preferred.to(device), view.to(device)
        with torch.set_grad_enabled(training):
            pred_a = model(image_a, metrics_a)
            pred_b = model(image_b, metrics_b)
            delta = pred_a["score"] - pred_b["score"]
            loss = F.softplus(-preferred * delta).mean()
            loss += 0.1 * (F.cross_entropy(pred_a["view_logits"], view) + F.cross_entropy(pred_b["view_logits"], view))
            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
        count += len(preferred)
        total += float(loss.item()) * len(preferred)
        correct += int(((delta.detach() * preferred) > 0).sum().item())
    return {"loss": total / count, "pair_accuracy": correct / count}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--pretrained", action="store_true", help="Download public ImageNet weights")
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        parser.error("epochs and batch size must be positive")
    random.seed(17)
    torch.manual_seed(17)
    train_rows, val_rows = load_rows(args.manifest)
    root = args.manifest.resolve().parent
    loaders = [
        DataLoader(PairDataset(rows, root), batch_size=args.batch_size, shuffle=shuffle, num_workers=0)
        for rows, shuffle in ((train_rows, True), (val_rows, False))
    ]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = PhotoRanker(pretrained=args.pretrained).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-4, weight_decay=1e-3)
    best_accuracy = -1.0
    for epoch in range(1, args.epochs + 1):
        train_metrics = run_epoch(model, loaders[0], optimizer, device)
        val_metrics = run_epoch(model, loaders[1], None, device)
        print(json.dumps({"epoch": epoch, "train": train_metrics, "val": val_metrics}))
        if val_metrics["pair_accuracy"] > best_accuracy:
            best_accuracy = val_metrics["pair_accuracy"]
            args.output.parent.mkdir(parents=True, exist_ok=True)
            torch.save({
                "model_state": model.state_dict(), "epoch": epoch,
                "view_names": VIEW_NAMES, "metric_names": METRIC_NAMES,
                "val_metrics": val_metrics, "architecture": "mobilenet_v3_small_pairwise_v1",
            }, args.output)


if __name__ == "__main__":
    main()
