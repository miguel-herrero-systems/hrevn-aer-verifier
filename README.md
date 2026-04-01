# HREVN™ AER Verifier

**Verify. Inspect. Trust.**

A Python plugin that gives AI agents structured, verifiable evidence to inspect, justify and reason over — without hallucinating on documents they cannot trust.

---

## Quickstart

```bash
git clone https://github.com/hrevn/aer-verifier
cd aer-verifier
python quickstart.py
```

No pip install. No configuration. No API keys.  
Python 3.10+ standard library only.

**Output:**

```
▶  Bundle 1 — Valid AER (privileged access change)
   Integrity:   ✔  VALID  (expected)
   Root hash:   match ✔
   AER ID:      AER-CAR-2026-002
   Artifacts:   12 total  [core: 4 | control: 1 | support: 4 | verification: 3]

▶  Bundle 2 — Tampered AER (operation_record modified)
   Integrity:   ✘  INVALID  (expected)
   ✘ checksum_mismatch: operation_record.json
   ✘ root_hash_mismatch: computed hash does not match declared

▶  Bundle 3 — Valid AER + Blockchain anchor (PII data export)
   Integrity:   ✔  VALID  (expected)
   Anchor:      ⛓  sepolia  0x7f3a2c1d8e4b9f0a6c...
```

---

## Tools

| Tool | What it does |
|---|---|
| `summarize_bundle` | Executive summary — **start here** |
| `verify_bundle` | Full integrity check: checksums + root hash |
| `inspect_manifest` | Read bundle metadata |
| `list_evidence` | List all artifacts with SHA-256 hashes |
| `check_anchor` | Check for external blockchain anchor |

### CLI usage

```bash
python main.py summarize_bundle source=demo/CAR-2026-002_valid.zip
python main.py verify_bundle    source=demo/CAR-2026-002_tampered.zip
python main.py list_evidence    source=demo/CAR-2026-003_anchored.zip
python main.py check_anchor     source=demo/CAR-2026-003_anchored.zip
```

### Python usage

```python
from tools import verify_bundle, summarize_bundle

result = verify_bundle("path/to/bundle.zip")
if result["valid"]:
    print("Bundle is intact. Root hash matches.")
else:
    print("Errors:", result["errors"])
```

All tools return JSON-serialisable dicts — designed for agent pipelines, not human parsing.

---

## What is an AER bundle?

An **Agent Evaluation Record (AER)** is a verifiable package documenting an AI agent operation:

```
bundle.zip
├── operation_record.json       ← what action the agent proposed
├── approval_record.json        ← who approved it and why
├── execution_record.json       ← outcome + cryptographic seal
├── agent_operation_review_report.pdf
├── manifest.json               ← structure + verification rules
├── CHECKSUMS.sha256            ← individual file hashes
├── ROOT_HASH_SHA256.txt        ← root hash of authoritative files
└── ANCHOR_SEPOLIA.json         ← (optional) blockchain timestamp
```

The root hash is computed deterministically from the authoritative files.  
Any alteration — even a single byte — produces a mismatch. The verifier detects it.

---

## Why this exists

AI agents are increasingly executing consequential actions: password resets, data exports, access changes, financial transactions.

When something goes wrong, the question is always the same:

> *"What exactly did the agent do, who approved it, and can you prove it wasn't modified after the fact?"*

Today that question has no good answer. AER bundles are the answer.

---

## EU AI Act

High-risk AI systems under **EU AI Act Article 9** must maintain logs of system operation sufficient to ensure traceability. The compliance deadline for most high-risk systems is **August 2026**.

AER bundles are designed as the verifiable operational record that satisfies this requirement:

- structured evidence of agent decisions
- human approval chain included
- cryptographic integrity (SHA-256, root hash)
- optional blockchain anchoring for non-repudiation
- machine-readable for automated compliance pipelines

---

## Architecture

```
hrevn_plugin/
├── main.py                  ← CLI entrypoint
├── quickstart.py            ← demo runner
├── demo/                    ← 3 demo bundles (valid / tampered / anchored)
├── tools/
│   ├── verify_bundle.py
│   ├── inspect_manifest.py
│   ├── list_evidence.py
│   ├── check_anchor.py
│   └── summarize_bundle.py
├── core/
│   ├── bundle_loader.py     ← ZIP + directory support
│   ├── hashing.py           ← SHA-256, root hash computation
│   ├── manifest_reader.py   ← manifest.json parser
│   └── checksum_validator.py
├── skills/                  ← Codex plugin skill definitions
└── .codex-plugin/
    └── plugin.json          ← Codex plugin manifest
```

**No external dependencies.** Python stdlib only.

---

## Codex plugin

This repo is structured as a Codex-compatible plugin.

To add to a local marketplace:

```json
// .agents/plugins/marketplace.json
{
  "plugins": [{
    "id": "hrevn-aer-verifier",
    "manifest": ".codex-plugin/plugin.json",
    "entry": "main.py"
  }]
}
```

Then in Codex: `/plugins` → install → `@hrevn-aer-verifier summarize_bundle source=...`

---

## Roadmap

- [x] v0.1 — Verify, inspect, list, anchor check, summarize
- [ ] v0.2 — AER bundle generator (API + CLI)
- [ ] v0.3 — Signed bundles (Ed25519)
- [ ] v0.4 — Live blockchain anchoring (Sepolia / Ethereum mainnet)
- [ ] v1.0 — Compliance API for EU AI Act Article 9

---

## License

| Component | License |
|---|---|
| Verifier code (`core/`, `tools/`, `main.py`) | MIT — see `LICENSE-VERIFIER` |
| AER format, manifest schema, ROOT_SPEC_AER_V1 | Proprietary — see `LICENSE-FORMAT` |
| HREVN trademark and certification mark | All rights reserved |

---

*Built to give AI agents something they urgently lack: structured, verifiable evidence they can inspect, justify and reason over.*
