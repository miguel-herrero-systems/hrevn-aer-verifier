"""
inspect_manifest.py
Return key metadata from manifest.json without full verification.
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core import load_bundle, BundleLoadError, parse_manifest, ManifestError
from core.hashing import sha256_bytes


def inspect_manifest(source: str) -> dict:
    result = {
        "tool": "inspect_manifest",
        "source": str(source),
        "ok": False,
        "error": None,
        "aer_id": None,
        "record_id": None,
        "workflow_id": None,
        "bundle_profile": None,
        "package_type": None,
        "package_family": None,
        "version": None,
        "generated_at_utc": None,
        "artifact_count": None,
        "root_scope_count": None,
        "checksum_scope_count": None,
        "verification_model": None,
        "signature_status": None,
        "external_anchor_status": None,
        "manifest_hash": None,
    }

    try:
        files = load_bundle(source)
    except BundleLoadError as e:
        result["error"] = str(e)
        return result

    if "manifest.json" not in files:
        result["error"] = "manifest.json not found in bundle"
        return result

    try:
        m = parse_manifest(files["manifest.json"])
    except ManifestError as e:
        result["error"] = str(e)
        return result

    result.update({
        "ok": True,
        "aer_id": m.aer_id,
        "record_id": m.record_id,
        "workflow_id": m.workflow_id,
        "bundle_profile": m.bundle_profile,
        "package_type": m.package_type,
        "package_family": m.package_family,
        "version": m.version,
        "generated_at_utc": m.generated_at_utc,
        "artifact_count": m.artifact_count,
        "root_scope_count": len(m.root_scope),
        "checksum_scope_count": len(m.checksum_scope),
        "verification_model": m.verification_model,
        "signature_status": m.signature_status,
        "external_anchor_status": m.external_anchor_status,
        "manifest_hash": sha256_bytes(files["manifest.json"]),
    })
    return result


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(inspect_manifest(src), indent=2))
