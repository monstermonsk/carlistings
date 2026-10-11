# Dealer connection setup: standard Crankshaft portal

This is the **fixed product setup screen**, not a custom dealer-system discovery questionnaire. The dealer chooses providers from the maintained [connector catalog](./Connector-Catalog-and-Dealer-Portal-Spec.md). Crankshaft applies the provider's versioned mapping preset. If a supported connection is unavailable, approved listings and call records remain available as CSV exports.

## Screen 1 — Dealership and locations

Dealer admin enters legal/display name, locations, timezone, website URL, dealer account/location IDs needed by selected providers, primary contact, and authorized approver. Existing Crankshaft identity provides login, tenant and roles. Every location has its own inbound DID/campaign mapping and default fallback destination. Validate location IDs before activation; the interface is the same for every dealer.

## Screen 2 — Sales team and call routing

Admin adds or imports each salesperson: name, active status, location(s), role, phone/transfer endpoint, availability schedule, routing priority and optional external CRM user ID. Crankshaft assigns an immutable `staff_id`. Test each destination and fallback through the **existing** router's approved configuration path. Effective-date status changes; keep historical call assignments when staff leave. Managers can inspect received calls, attempts, actual answered agent, missed/fallback calls, qualification, vehicle interest and CRM lead/outcome receipts in the Crankshaft portal. Caller data is masked by role.

## Screen 3 — Inventory, CRM and publication connections

Admin selects provider **and product** for (a) inventory/DMS, (b) CRM, (c) website/syndicator, and (d) optional direct destinations. The portal shows the catalog's actual capabilities and prerequisites. It offers vendor OAuth when supported, a one-time API token input where a vendor issues one, or a partner-access pending state. Credentials enter the vault; the portal shows only connection status, scopes and last test. Admin grants required dealer permissions with the vendor. Crankshaft tests a read-only stock/lead sample or provider sandbox, displays mapping preview, and activates only supported directions. A dealer account cannot create an API that the vendor has not exposed.

## Screen 4 — Listing policy and outputs

Admin confirms stock/price/status authority, listing disclosures, approver role, destinations, approved call tracking number, expected photo/video limits and import/export cadence. These are standard fields, not a software inspection. For unsupported vendor routes, choose **Download CSV + media ZIP** or **authorized SFTP delivery**. CSV creation creates an `exported` receipt; dealer/importer acknowledgment and live link are separately recorded. The portal reports whether each listing is `draft`, `approved`, `accepted`, `live`, `live unverified`, `exported`, `failed` or `withdrawn`.

## Screen 5 — Test and activate

Run a stock read, one sample listing export, connection permission test, call transfer/answer/fallback test, CRM lead push if supported, and appointment/outcome read or CSV import test. Activation records the admin, provider manifest version, mapping preset, test receipts and date. Reauthorization, secret rotation and disabling a connection use the same screen. A failed connector never interrupts live calls; the portal shows action and CSV remains available.

## Required admin inputs (standard schema)

| Field | Validation / purpose |
|---|---|
| `dealer_name`, `location_id`, `timezone`, `website_url` | Stable tenant/location and live VDP mapping. |
| `inventory_provider`, `inventory_product`, `vendor_dealer_id` | Selects supported adapter manifest and stock mapping preset. |
| `crm_provider`, `crm_product`, `vendor_location_id` | Selects lead/outcome route; optional. |
| `website_or_syndicator_provider` | Primary approved publishing route; optional when CSV-only. |
| `staff[]` | Name, stable Crankshaft ID, location, active dates, route target, schedule, optional CRM user ID. |
| `routing_policy` | Priority/round robin, timeout, no-answer fallback, service/after-hours path. Existing router executes it. |
| `approval_policy`, `required_disclosures` | Dealer authority and versioned listing gate. |
| `provider_authorization` | OAuth grant, API token or partner pending; secret itself never stored in this form. |
| `export_mode` | Download or approved SFTP; CSV format and receipt options. |

## Go/no-go

The staff directory and call ledger can launch with a CSV-only listing route. To enable any vendor write path, require dealer authorization, a successful provider test, scope/tenant match, field mapping validation, an approved listing version and an external receipt. To mark a listing live, verify the provider record or public VDP. To enable CRM writes, prove lead receipt and duplicate suppression. To enable call reporting, replay transfer attempts/answers and show the same agent in the portal as in SignalWire. Maintain a per-connection kill switch and audit trail.
