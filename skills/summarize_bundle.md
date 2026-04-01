# summarize_bundle

**Tool:** `summarize_bundle`  
**Plugin:** HREVN AER Verifier

## What it does

Produces a structured executive summary of an HREVN bundle in a single call.
Combines identity, artifact breakdown, integrity status and anchor status.

Use this as the first call when you receive an unknown bundle and need a fast overview before deeper analysis.

## Input

```
source: string  — path to .zip bundle OR path to extracted bundle directory
```

## Output (JSON)

```json
{
  "tool": "summarize_bundle",
  "source": "<path>",
  "ok": true,
  "identity": {
    "aer_id": "AER-CAR-2026-002",
    "record_id": "CAR-2026-002",
    "workflow_id": "WF-IAM-2026-002",
    "bundle_profile": "agent_operation_aer_v1",
    "package_family": "hrevn_aer",
    "version": "aer_demo_v1",
    "generated_at_utc": "2026-04-01T08:44:30Z"
  },
  "artifacts": {
    "total": 12,
    "declared_in_manifest": 12,
    "by_category": {
      "core": 4,
      "control": 1,
      "verification": 3,
      "support": 4
    },
    "has_pdf_report": true,
    "has_checksums": true,
    "has_root_hash": true
  },
  "integrity": {
    "valid": true,
    "root_hash_match": true,
    "errors": [],
    "warnings": ["unsigned_bundle: unsigned_demo"]
  },
  "anchor": {
    "anchor_present": false,
    "anchor_file": null,
    "anchor_status_manifest": "not_anchored"
  },
  "status": {
    "signature": "unsigned_demo",
    "passes_basic_verification": true,
    "is_demo": true,
    "is_anchored": false
  }
}
```

## Recommended workflow

1. `summarize_bundle` — fast overview
2. `verify_bundle` — full integrity check if needed
3. `list_evidence` — enumerate artifacts before reasoning

## Example invocation

```
@hrevn-aer-verifier summarize_bundle source=/path/to/bundle.zip
```
