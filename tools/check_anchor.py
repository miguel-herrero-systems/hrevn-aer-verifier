"""Inspect optional anchor metadata embedded in an AER bundle.

This module does not query a blockchain node and does not establish inclusion,
canonical-chain membership, confirmations, or finality.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core import BundleLoadError, ManifestError, load_bundle, parse_manifest


KNOWN_ANCHOR_FILES = [
    "ANCHOR_SEPOLIA.json",
    "ANCHOR_MAINNET.json",
    "ANCHOR_ETHEREUM.json",
    "ANCHOR_POLYGON.json",
    "ANCHOR.json",
]


def check_anchor(source: str) -> dict:
    """Report the presence and parseability of embedded anchor metadata only."""

    result = {
        "tool": "check_anchor",
        "source": str(source),
        "ok": False,
        "error": None,
        "verification_scope": "metadata_presence_only",
        "on_chain_verification_performed": False,
        "anchor_present": False,
        "anchor_file": None,
        "anchor_status_manifest": None,
        "anchor_data": None,
    }

    try:
        files = load_bundle(source)
    except BundleLoadError as exc:
        result["error"] = str(exc)
        return result

    result["ok"] = True

    if "manifest.json" in files:
        try:
            manifest = parse_manifest(files["manifest.json"])
            result["anchor_status_manifest"] = manifest.external_anchor_status
        except ManifestError:
            pass

    for candidate in KNOWN_ANCHOR_FILES:
        if candidate not in files:
            continue
        result["anchor_present"] = True
        result["anchor_file"] = candidate
        try:
            result["anchor_data"] = json.loads(files[candidate].decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            result["error"] = f"anchor_metadata_parse_error: {exc}"
            result["ok"] = False
        return result

    for filename in files:
        if "anchor" in filename.lower() and filename != "manifest.json":
            result["anchor_present"] = True
            result["anchor_file"] = filename
            break

    return result


if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(check_anchor(source), indent=2))
