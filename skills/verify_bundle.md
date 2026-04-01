# verify_bundle

**Tool:** `verify_bundle`  
**Plugin:** HREVN AER Verifier

## What it does

Verifies the integrity of an HREVN AER bundle (ZIP file or extracted directory).

Checks:
- All files match their declared SHA-256 checksums
- The root hash computed from `root_scope` matches `ROOT_HASH_SHA256.txt`
- `manifest.json` is present and parseable
- No declared files are missing

## When to use

Use this tool before reasoning over any HREVN bundle. It tells you whether the package is intact and unaltered.

## Input

```
source: string  — path to .zip bundle OR path to extracted bundle directory
```

## Output (JSON)

```json
{
  "tool": "verify_bundle",
  "source": "<path>",
  "valid": true,
  "errors": [],
  "warnings": ["unsigned_bundle: unsigned_demo", "not_anchored: no external blockchain anchor"],
  "schema_version": "aer_demo_v1",
  "manifest_hash": "<sha256>",
  "root_hash_declared": "<sha256>",
  "root_hash_computed": "<sha256>",
  "root_hash_match": true,
  "checksums": {
    "valid": true,
    "passed": ["operation_record.json", "..."],
    "failed": [],
    "missing": [],
    "unchecked": []
  },
  "artifact_count": 12,
  "aer_id": "AER-CAR-2026-002"
}
```

## Key fields

| Field | Meaning |
|---|---|
| `valid` | `true` only if zero errors |
| `root_hash_match` | Whether root hash recomputation matches declared |
| `errors` | Hard failures (tampered file, missing file, hash mismatch) |
| `warnings` | Soft notices (unsigned, not anchored) |

## Example invocation

```
@hrevn-aer-verifier verify_bundle source=/path/to/bundle.zip
```
