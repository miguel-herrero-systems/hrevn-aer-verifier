# check_anchor

**Tool:** `check_anchor`  
**Plugin:** HREVN AER Verifier

## What it does

Checks whether the bundle contains an external anchor (e.g. blockchain timestamp — Sepolia, Ethereum, Polygon).

## Input

```
source: string  — path to .zip bundle OR path to extracted bundle directory
```

## Output (JSON)

```json
{
  "tool": "check_anchor",
  "source": "<path>",
  "ok": true,
  "anchor_present": false,
  "anchor_file": null,
  "anchor_status_manifest": "not_anchored",
  "anchor_data": null
}
```

If anchor is present:
```json
{
  "anchor_present": true,
  "anchor_file": "ANCHOR_SEPOLIA.json",
  "anchor_data": {
    "chain": "sepolia",
    "tx_hash": "0x...",
    "block": 12345678,
    "timestamp_utc": "2026-04-01T10:00:00Z"
  }
}
```

## Example invocation

```
@hrevn-aer-verifier check_anchor source=/path/to/bundle.zip
```
