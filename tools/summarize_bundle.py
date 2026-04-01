"""
summarize_bundle.py
Generate a structured executive summary of an HREVN bundle.
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core import load_bundle, BundleLoadError, parse_manifest, ManifestError
from tools.verify_bundle import verify_bundle
from tools.check_anchor import check_anchor


def summarize_bundle(source: str) -> dict:
    result = {
        "tool": "summarize_bundle",
        "source": str(source),
        "ok": False,
        "error": None,
        "identity": {},
        "integrity": {},
        "artifacts": {},
        "anchor": {},
        "status": {},
    }

    try:
        files = load_bundle(source)
    except BundleLoadError as e:
        result["error"] = str(e)
        return result

    # Identity from manifest
    if "manifest.json" not in files:
        result["error"] = "manifest.json not found"
        return result

    try:
        m = parse_manifest(files["manifest.json"])
    except ManifestError as e:
        result["error"] = str(e)
        return result

    result["identity"] = {
        "aer_id": m.aer_id,
        "record_id": m.record_id,
        "workflow_id": m.workflow_id,
        "bundle_profile": m.bundle_profile,
        "package_family": m.package_family,
        "version": m.version,
        "generated_at_utc": m.generated_at_utc,
    }

    # Artifact breakdown by category
    categories = {}
    for a in m.artifacts:
        cat = a.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    has_pdf = any(f.endswith(".pdf") for f in files)
    has_checksums = "CHECKSUMS.sha256" in files
    has_root_hash = "ROOT_HASH_SHA256.txt" in files

    result["artifacts"] = {
        "total": len(files),
        "declared_in_manifest": m.artifact_count,
        "by_category": categories,
        "has_pdf_report": has_pdf,
        "has_checksums": has_checksums,
        "has_root_hash": has_root_hash,
    }

    # Quick integrity check (reuse verify_bundle)
    vr = verify_bundle(source)
    result["integrity"] = {
        "valid": vr["valid"],
        "root_hash_match": vr.get("root_hash_match", False),
        "errors": vr["errors"],
        "warnings": vr["warnings"],
    }

    # Anchor
    ar = check_anchor(source)
    result["anchor"] = {
        "anchor_present": ar["anchor_present"],
        "anchor_file": ar["anchor_file"],
        "anchor_status_manifest": ar["anchor_status_manifest"],
    }

    # Status flags
    result["status"] = {
        "signature": m.signature_status,
        "passes_basic_verification": vr["valid"],
        "is_demo": "demo" in m.version.lower() or "demo" in m.package_type.lower(),
        "is_anchored": ar["anchor_present"],
    }

    result["ok"] = True
    return result


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(summarize_bundle(src), indent=2))
