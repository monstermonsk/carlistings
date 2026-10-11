"""Free vPIC identity lookup. A decode never confirms installed options."""

from __future__ import annotations

import json
import re
from typing import Callable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

VIN_RE = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")
BASE = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValuesExtended/"
IDENTITY_FIELDS = (
    "VIN", "ModelYear", "Make", "Model", "Trim", "Series", "VehicleType",
    "BodyClass", "DriveType", "FuelTypePrimary", "EngineCylinders",
    "DisplacementL", "Manufacturer", "PlantCountry",
)


def _download(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "Crankshaft-Listing-Tuner/0.1"})
    with urlopen(request, timeout=12) as response:
        return json.load(response)


def decode_vin(
    vin: str,
    model_year: int | None = None,
    fetch_json: Callable[[str], dict] | None = None,
) -> dict:
    """Return identity candidates and decoder diagnostics, with zero option claims.

    The caller stores the raw response separately for audit, caches by VIN/year,
    and reconciles these candidates against the dealer's inventory record.
    """
    normalized = vin.strip().upper()
    if not VIN_RE.fullmatch(normalized):
        raise ValueError("VIN must contain 17 valid VIN characters")
    if model_year is not None and not 1900 <= model_year <= 2100:
        raise ValueError("model_year is outside the supported planning range")
    query = {"format": "json"}
    if model_year is not None:
        query["modelyear"] = str(model_year)
    url = f"{BASE}{normalized}?{urlencode(query)}"
    payload = (fetch_json or _download)(url)
    rows = payload.get("Results")
    if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict):
        raise ValueError("Unexpected vPIC response shape")
    row = rows[0]
    fields = {name: str(row[name]).strip() for name in IDENTITY_FIELDS if row.get(name) not in (None, "")}
    error_code = str(row.get("ErrorCode", "")).strip()
    return {
        "vin": normalized,
        "provider": "nhtsa_vpic",
        "status": "decoded" if error_code == "0" else "review_required",
        "identity_candidates": fields,
        "installed_options": [],
        "installed_options_verified": False,
        "decoder_error_code": error_code,
        "decoder_error_text": str(row.get("ErrorText", "")),
        "request_url": url,
    }
