# list_evidence

**Tool:** `list_evidence`  
**Plugin:** HREVN AER Verifier

## What it does

Lists every artifact in the bundle with its SHA-256 hash, size, category and role as declared in `manifest.json`.

Use this when you need to know exactly what evidence a bundle contains before reasoning over it.

## Input

```
source: string  — path to .zip bundle OR path to extracted bundle directory
```

## Output (JSON)

```json
{
  "tool": "list_evidence",
  "source": "<path>",
  "ok": true,
  "total_files": 12,
  "artifacts": [
    {
      "file": "operation_record.json",
      "size_bytes": 705,
      "sha256": "<sha256>",
      "category": "core",
      "role": "structured_operation_record",
      "in_root_scope": true,
      "in_checksum_scope": true
    },
    {
      "file": "approval_record.json",
      "size_bytes": 371,
      "sha256": "<sha256>",
      "category": "core",
      "role": "human_approval_record",
      "in_root_scope": true,
      "in_checksum_scope": true
    }
  ]
}
```

## Key fields per artifact

| Field | Meaning |
|---|---|
| `category` | `core`, `control`, `verification`, `support` |
| `role` | Semantic function within the bundle |
| `in_root_scope` | Included in root hash calculation |
| `in_checksum_scope` | Included in CHECKSUMS.sha256 |

## Example invocation

```
@hrevn-aer-verifier list_evidence source=/path/to/bundle.zip
```
