"""
test_plugin.py
Tests against the real bundle CAR-2026-002 and two broken variants.
Run: python tests/test_plugin.py
"""

import sys, os, json, zipfile, shutil, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools import verify_bundle, inspect_manifest, list_evidence, check_anchor, summarize_bundle

REAL_BUNDLE = "/mnt/user-data/uploads/1775033137551_CAR-2026-002_20260401_084430_c7ee454221ad8dd18ea9cae2b882ab72f973cd68c59b928601682614eff10bee.zip"

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"


def check(label, condition, detail=""):
    if condition:
        print(f"  {PASS}  {label}")
    else:
        print(f"  {FAIL}  {label}  {detail}")
    return condition


def make_broken_bundle_tampered(src_zip: str, tmp_dir: str) -> str:
    """Copy bundle but corrupt operation_record.json content."""
    out = os.path.join(tmp_dir, "broken_tampered.zip")
    with zipfile.ZipFile(src_zip, "r") as zin, zipfile.ZipFile(out, "w") as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "operation_record.json":
                data = data.replace(b"force_reset", b"TAMPERED_!")
            zout.writestr(item, data)
    return out


def make_broken_bundle_missing_file(src_zip: str, tmp_dir: str) -> str:
    """Copy bundle but omit ROOT_HASH_SHA256.txt."""
    out = os.path.join(tmp_dir, "broken_missing.zip")
    with zipfile.ZipFile(src_zip, "r") as zin, zipfile.ZipFile(out, "w") as zout:
        for item in zin.infolist():
            if item.filename == "ROOT_HASH_SHA256.txt":
                continue
            zout.writestr(item, zin.read(item.filename))
    return out


def run_tests():
    tmp = tempfile.mkdtemp()
    try:
        print("\n═══ TEST SUITE: HREVN Plugin Core ═══\n")

        # ── 1. verify_bundle (valid) ──────────────────────────────────────
        print("1. verify_bundle — real bundle")
        vr = verify_bundle(REAL_BUNDLE)
        check("valid=True", vr["valid"])
        check("root_hash_match=True", vr["root_hash_match"])
        check("no errors", len(vr["errors"]) == 0, str(vr["errors"]))
        check("aer_id present", vr["aer_id"] == "AER-CAR-2026-002")

        # ── 2. verify_bundle (tampered) ───────────────────────────────────
        print("\n2. verify_bundle — tampered bundle")
        broken_t = make_broken_bundle_tampered(REAL_BUNDLE, tmp)
        vt = verify_bundle(broken_t)
        check("valid=False (tampered)", not vt["valid"])
        check("has checksum_mismatch error", any("checksum_mismatch" in e for e in vt["errors"]))
        check("root_hash_match=False", not vt["root_hash_match"])

        # ── 3. verify_bundle (missing file) ──────────────────────────────
        print("\n3. verify_bundle — missing ROOT_HASH_SHA256.txt")
        broken_m = make_broken_bundle_missing_file(REAL_BUNDLE, tmp)
        vm = verify_bundle(broken_m)
        check("warning about missing root hash", any("missing_root_hash" in w for w in vm["warnings"]))

        # ── 4. inspect_manifest ───────────────────────────────────────────
        print("\n4. inspect_manifest")
        im = inspect_manifest(REAL_BUNDLE)
        check("ok=True", im["ok"])
        check("aer_id", im["aer_id"] == "AER-CAR-2026-002")
        check("record_id", im["record_id"] == "CAR-2026-002")
        check("bundle_profile", im["bundle_profile"] == "agent_operation_aer_v1")
        check("artifact_count=12", im["artifact_count"] == 12)
        check("manifest_hash present", bool(im["manifest_hash"]))

        # ── 5. list_evidence ──────────────────────────────────────────────
        print("\n5. list_evidence")
        le = list_evidence(REAL_BUNDLE)
        check("ok=True", le["ok"])
        check("total_files=12", le["total_files"] == 12)
        core_files = [a for a in le["artifacts"] if a["category"] == "core"]
        check("4 core artifacts", len(core_files) == 4)
        check("all have sha256", all(len(a["sha256"]) == 64 for a in le["artifacts"]))

        # ── 6. check_anchor ───────────────────────────────────────────────
        print("\n6. check_anchor")
        ca = check_anchor(REAL_BUNDLE)
        check("ok=True", ca["ok"])
        check("anchor_present=False (demo)", not ca["anchor_present"])
        check("manifest says not_anchored", ca["anchor_status_manifest"] == "not_anchored")

        # ── 7. summarize_bundle ───────────────────────────────────────────
        print("\n7. summarize_bundle")
        sb = summarize_bundle(REAL_BUNDLE)
        check("ok=True", sb["ok"])
        check("passes_basic_verification", sb["status"]["passes_basic_verification"])
        check("is_demo=True", sb["status"]["is_demo"])
        check("identity has aer_id", sb["identity"]["aer_id"] == "AER-CAR-2026-002")
        check("artifacts.total=12", sb["artifacts"]["total"] == 12)

        print("\n═══ DONE ═══\n")

    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    run_tests()
