# inspect_manifest

**Tool:** `inspect_manifest`  
**Plugin:** HREVN AER Verifier

## What it does

Reads `manifest.json` from an HREVN bundle and returns structured metadata — without running full verification.

Use this for a fast overview of what a bundle contains and who generated it.

## Input

```
source: string  — path to .zip bundle OR path to extracted bundle directory
```

## Output (JSON)

```json
{
  "tool": "inspect_manifest",
  "source": "<path>",
  "ok": true,
  "aer_id": "AER-CAR-2026-002",
  "record_id": "CAR-2026-002",
  "workflow_id": "WF-IAM-2026-002",
  "bundle_profile": "agent_operation_aer_v1",
  "package_type": "agent_operation_aer_demo_v1",
  "package_family": "hrevn_aer",
  "version": "aer_demo_v1",
  "generated_at_utc": "2026-04-01T08:44:30Z",
  "artifact_count": 12,
  "root_scope_count": 5,
  "checksum_scope_count": 11,
  "verification_model": "ROOT_AER_V1",
  "signature_status": "unsigned_demo",
  "external_anchor_status": "not_anchored",
  "manifest_hash": "<sha256>"
}
```

## Example invocation

```
@hrevn-aer-verifier inspect_manifest source=/path/to/bundle.zip
```
