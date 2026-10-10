"""Validate the public, rights-safe review package after cloning or downloading."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import csv

root = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.cards = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "article" and "listing" in attrs.get("class", "").split():
            self.cards += 1
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


issues = []
for path in root.rglob("*.html"):
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    for ref in page.links:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.is_relative_to(root) or not target.is_file():
            issues.append(f"Broken link: {path.relative_to(root)} -> {ref}")

gallery = Page()
gallery.feed((root / "samples/index.html").read_text(encoding="utf-8"))
if gallery.cards != 40:
    issues.append(f"Expected 40 listing cards, found {gallery.cards}")
rows = list(csv.DictReader((root / "samples/listings.tsv").open(encoding="utf-8"), delimiter="\t"))
if len(rows) != 40 or len({row["id"] for row in rows}) != 40:
    issues.append("Expected 40 unique listing rows")
if list(root.rglob("*.avif")):
    issues.append("Third-party AVIF photo files must not be in the public package")
for name in (
    "plan/Crankshaft-Business-Plan.pdf",
    "plan/Crankshaft-Business-Model.pdf",
    "plan/Crankshaft-Investor-Brief.pdf",
    "sales/Crankshaft-Dealer-Service-Guide.pdf",
    "financials/Crankshaft-24-Month-Model.xlsx",
):
    if not (root / name).is_file():
        issues.append(f"Missing document: {name}")
if issues:
    raise SystemExit("\n".join(issues))
print(f"Public package verified: {gallery.cards} cards, {len(rows)} data rows, links and documents; no marketplace photo files")
