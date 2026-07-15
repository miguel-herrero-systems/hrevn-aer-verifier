# HREVN AER Verifier

Experimental, standard-library Python tools for inspecting the internal integrity of HREVN Agent Evaluation Record (AER) bundles.

**Status:** public technical alpha. The included bundles and anchor metadata are synthetic test fixtures.

## What the verifier establishes

- bundle files can be loaded from a ZIP archive or directory
- declared SHA-256 checksums match the included bytes
- the deterministic root hash can be recomputed from the declared root scope
- manifest metadata and evidence inventory can be inspected
- optional anchor metadata is present and parseable

## What it does not establish

- authorship or signer identity
- validity of a digital signature
- truth or semantic correctness of the recorded event
- inclusion of a root hash in an Ethereum transaction
- transaction finality or canonical-chain membership
- regulatory compliance

`check_anchor` currently reports and parses anchor metadata. It does **not** query an RPC endpoint, retrieve a receipt, validate calldata, or establish finality.

## Quickstart

```bash
git clone https://github.com/miguel-herrero-systems/hrevn-aer-verifier.git
cd hrevn-aer-verifier
python3 quickstart.py
python3 -m unittest discover -s tests -v
```

No API key or third-party Python dependency is required for the local demonstration.

## Tools

| Tool | Result |
|---|---|
| `summarize_bundle` | Compact structural and integrity summary |
| `verify_bundle` | Checksum and deterministic root-hash verification |
| `inspect_manifest` | Parsed manifest metadata |
| `list_evidence` | Artifact inventory and declared hashes |
| `check_anchor` | Presence and parsing of anchor metadata; no chain verification |

Example:

```bash
python3 main.py verify_bundle source=demo/CAR-2026-002_valid.zip
python3 main.py verify_bundle source=demo/CAR-2026-002_tampered.zip
python3 main.py check_anchor source=demo/CAR-2026-003_anchored.zip
```

All tool results are JSON-serializable dictionaries.

## Demonstration fixtures

The `demo/` directory contains synthetic fixtures for three behaviors:

1. internally consistent bundle
2. bundle whose operation record was altered
3. internally consistent bundle containing synthetic Sepolia-style anchor metadata

The transaction hash, block number, timestamps, identities, and operational events in these fixtures must not be interpreted as production evidence or as proof of an on-chain transaction.

## Regulatory context

The EU AI Act separates several obligations that are sometimes conflated: Article 9 addresses risk management, Article 12 addresses automatic record-keeping capabilities for high-risk systems, and Article 19 addresses retention of automatically generated logs by providers where those logs are under their control.

AER bundles may support documentation, traceability, or review processes. This repository does not determine whether a system is high-risk and does not claim that using the format satisfies any legal obligation. Legal and compliance conclusions require an independent assessment of the complete system and its intended use.

## Architecture

```text
main.py              command entry point
quickstart.py        local synthetic demonstration
core/                loading, manifest parsing, checksums, root hashing
tools/               structured inspection functions
tests/               reproducible tests using bundled fixtures
demo/                synthetic fixtures
skills/              agent-facing usage instructions
```

## License

- Verifier software: MIT; see `LICENSE-VERIFIER`.
- AER format and demo fixtures: separate terms; see `LICENSE-FORMAT`.
- HREVN name and marks: all rights reserved.

See `LICENSE.md` for the repository-level scope map. Questions about licensing should use [contact@hrevn.com](mailto:contact@hrevn.com). The license documents, not this summary, control.

## Security

Do not disclose suspected vulnerabilities in a public issue. Follow the repository security policy or email [contact@hrevn.com](mailto:contact@hrevn.com) with the subject `[SECURITY] hrevn-aer-verifier`.
