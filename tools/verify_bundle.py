"""
verify_bundle.py
Full integrity verification of an HREVN bundle.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core import (
    load_bundle, BundleLoadError,
    parse_manifest, ManifestError,
    parse_checksums, validate_checksums,
    compute_root_hash,
)


def verify_bundle(source: str) -> dict:
    """
    Verify an HREVN bundle (ZIP or directory).
    Returns a structured JSON-serialisable result.
    """
    result = {
        "tool": "verify_bundle",
        "source": str(source),
        "valid": False,
        "errors": [],
        "warnings": [],
        "schema_version": None,
        "manifest_hash": None,
        "root_hash_declared": None,
        "root_hash_computed": None,
        "root_hash_match": False,
        "checksums": None,
        "artifact_count": None,
        "aer_id": None,
    }

    # 1. Load
    try:
        files = load_bundle(source)
    except BundleLoadError as e:
        result["errors"].append(f"load_error: {e}")
        return result

    # 2. Manifest
    if "manifest.json" not in files:
        result["errors"].append("missing_manifest: manifest.json not found")
        return result

    try:
        manifest = parse_manifest(files["manifest.json"])
    except ManifestError as e:
        result["errors"].append(f"manifest_parse_error: {e}")
        return result

    from core.hashing import sha256_bytes
    result["manifest_hash"] = sha256_bytes(files["manifest.json"])
    result["schema_version"] = manifest.version
    result["artifact_count"] = manifest.artifact_count
    result["aer_id"] = manifest.aer_id

    # 3. Checksums
    if "CHECKSUMS.sha256" not in files:
        result["errors"].append("missing_checksums: CHECKSUMS.sha256 not found")
    else:
        try:
            expected = parse_checksums(files["CHECKSUMS.sha256"])
            cs_result = validate_checksums(files, expected)
            result["checksums"] = cs_result
            if not cs_result["valid"]:
                for f in cs_result["failed"]:
                    result["errors"].append(f"checksum_mismatch: {f['file']}")
                for f in cs_result["missing"]:
                    result["errors"].append(f"missing_file: {f}")
            if cs_result["unchecked"]:
                for f in cs_result["unchecked"]:
                    result["warnings"].append(f"unchecked_file: {f}")
        except Exception as e:
            result["errors"].append(f"checksum_parse_error: {e}")

    # 4. Root hash
    if "ROOT_HASH_SHA256.txt" not in files:
        result["warnings"].append("missing_root_hash_file: ROOT_HASH_SHA256.txt not found")
    else:
        declared = files["ROOT_HASH_SHA256.txt"].decode("utf-8").strip()
        result["root_hash_declared"] = declared
        try:
            computed = compute_root_hash(
                files,
                manifest.root_scope,
                manifest.root_serialization,
            )
            result["root_hash_computed"] = computed
            result["root_hash_match"] = (computed == declared)
            if not result["root_hash_match"]:
                result["errors"].append("root_hash_mismatch: computed hash does not match declared")
        except KeyError as e:
            result["errors"].append(f"root_hash_error: {e}")

    # 5. Warnings
    if manifest.signature_status and "unsigned" in manifest.signature_status:
        result["warnings"].append(f"unsigned_bundle: {manifest.signature_status}")
    if manifest.external_anchor_status == "not_anchored":
        result["warnings"].append("not_anchored: no external blockchain anchor")

    # 6. Final verdict
    result["valid"] = len(result["errors"]) == 0

    return result


if __name__ == "__main__":
    import json
    src = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(verify_bundle(src), indent=2))
