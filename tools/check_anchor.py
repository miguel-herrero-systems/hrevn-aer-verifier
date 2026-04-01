"""
check_anchor.py
Check whether the bundle contains an external anchor (e.g. blockchain).
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core import load_bundle, BundleLoadError, parse_manifest, ManifestError

KNOWN_ANCHOR_FILES = [
    "ANCHOR_SEPOLIA.json",
    "ANCHOR_MAINNET.json",
    "ANCHOR_ETHEREUM.json",
    "ANCHOR_POLYGON.json",
    "ANCHOR.json",
]


def check_anchor(source: str) -> dict:
    result = {
        "tool": "check_anchor",
        "source": str(source),
        "ok": False,
        "error": None,
        "anchor_present": False,
        "anchor_file": None,
        "anchor_status_manifest": None,
        "anchor_data": None,
    }

    try:
        files = load_bundle(source)
    except BundleLoadError as e:
        result["error"] = str(e)
        return result

    result["ok"] = True

    # Check manifest declaration
    if "manifest.json" in files:
        try:
            m = parse_manifest(files["manifest.json"])
            result["anchor_status_manifest"] = m.external_anchor_status
        except ManifestError:
            pass

    # Look for known anchor files
    for candidate in KNOWN_ANCHOR_FILES:
        if candidate in files:
            result["anchor_present"] = True
            result["anchor_file"] = candidate
            try:
                result["anchor_data"] = json.loads(files[candidate].decode("utf-8"))
            except Exception:
                result["anchor_data"] = {"raw": files[candidate].decode("utf-8", errors="replace")}
            break

    # Also scan for any file with "anchor" in the name
    if not result["anchor_present"]:
        for fname in files:
            if "anchor" in fname.lower() and fname != "manifest.json":
                result["anchor_present"] = True
                result["anchor_file"] = fname
                break

    return result


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(check_anchor(src), indent=2))
