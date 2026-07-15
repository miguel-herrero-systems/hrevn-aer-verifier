---
name: inspect-aer-bundles
description: Inspect HREVN Agent Evaluation Record bundles with the bundled Python verifier. Use when Codex needs to summarize an AER bundle, verify its internal checksums and deterministic root hash, inventory evidence, inspect its manifest, or report embedded anchor metadata without making an on-chain or regulatory-compliance claim.
---

# Inspect AER bundles

Work from the plugin root containing `main.py`. Accept a ZIP bundle or an extracted bundle directory supplied by the user.

## Workflow

1. Start with a structural summary:

   ```bash
   python3 main.py summarize_bundle source="<bundle-path>"
   ```

2. Run the focused command needed for the question:

   ```bash
   python3 main.py verify_bundle source="<bundle-path>"
   python3 main.py inspect_manifest source="<bundle-path>"
   python3 main.py list_evidence source="<bundle-path>"
   python3 main.py check_anchor source="<bundle-path>"
   ```

3. Report executed output separately from interpretation. Preserve errors and warnings in the result.

## Boundaries

- Treat `verify_bundle` as an internal byte-integrity check only.
- Do not infer authorship, signer identity, event truth, or semantic correctness from matching hashes.
- Treat `check_anchor` as metadata inspection only. It does not query a node or establish transaction inclusion, canonical-chain membership, confirmations, or finality.
- Do not infer regulatory compliance from any successful command.
- Identify the included demo bundles and their anchor metadata as synthetic fixtures.
