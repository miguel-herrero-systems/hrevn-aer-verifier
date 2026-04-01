"""
list_evidence.py
List all artifacts in the bundle with hashes, sizes and roles.
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core import load_bundle, BundleLoadError, parse_manifest, ManifestError
from core.hashing import sha256_bytes


def list_evidence(source: str) -> dict:
    result = {
        "tool": "list_evidence",
        "source": str(source),
        "ok": False,
        "error": None,
        "total_files": 0,
        "artifacts": [],
    }

    try:
        files = load_bundle(source)
    except BundleLoadError as e:
        result["error"] = str(e)
        return result

    # Build role map from manifest if available
    role_map = {}
    category_map = {}
    in_root_scope = set()
    in_checksum_scope = set()

    if "manifest.json" in files:
        try:
            m = parse_manifest(files["manifest.json"])
            for a in m.artifacts:
                role_map[a["artifact"]] = a.get("role", "")
                category_map[a["artifact"]] = a.get("category", "")
            in_root_scope = set(m.root_scope)
            in_checksum_scope = set(m.checksum_scope)
        except ManifestError:
            pass

    artifacts = []
    for fname, data in sorted(files.items()):
        artifacts.append({
            "file": fname,
            "size_bytes": len(data),
            "sha256": sha256_bytes(data),
            "category": category_map.get(fname, "unknown"),
            "role": role_map.get(fname, ""),
            "in_root_scope": fname in in_root_scope,
            "in_checksum_scope": fname in in_checksum_scope,
        })

    result["ok"] = True
    result["total_files"] = len(artifacts)
    result["artifacts"] = artifacts
    return result


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(list_evidence(src), indent=2))
