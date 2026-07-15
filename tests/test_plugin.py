from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from tools import check_anchor, inspect_manifest, list_evidence, summarize_bundle, verify_bundle


VALID_BUNDLE = REPOSITORY_ROOT / "demo" / "CAR-2026-002_valid.zip"
TAMPERED_BUNDLE = REPOSITORY_ROOT / "demo" / "CAR-2026-002_tampered.zip"
ANCHORED_FIXTURE = REPOSITORY_ROOT / "demo" / "CAR-2026-003_anchored.zip"


class AERVerifierTests(unittest.TestCase):
    def test_valid_fixture_passes_internal_integrity_checks(self) -> None:
        result = verify_bundle(str(VALID_BUNDLE))
        self.assertTrue(result["valid"])
        self.assertTrue(result["root_hash_match"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["aer_id"], "AER-CAR-2026-002")

    def test_tampered_fixture_fails_checksum_and_root_hash(self) -> None:
        result = verify_bundle(str(TAMPERED_BUNDLE))
        self.assertFalse(result["valid"])
        self.assertFalse(result["root_hash_match"])
        self.assertTrue(any("checksum_mismatch" in error for error in result["errors"]))
        self.assertTrue(any("root_hash_mismatch" in error for error in result["errors"]))

    def test_manifest_and_evidence_are_inspectable(self) -> None:
        manifest = inspect_manifest(str(VALID_BUNDLE))
        evidence = list_evidence(str(VALID_BUNDLE))
        self.assertTrue(manifest["ok"])
        self.assertEqual(manifest["aer_id"], "AER-CAR-2026-002")
        self.assertTrue(evidence["ok"])
        self.assertEqual(evidence["total_files"], 12)
        self.assertTrue(all(len(item["sha256"]) == 64 for item in evidence["artifacts"]))

    def test_anchor_tool_reports_metadata_presence_only(self) -> None:
        result = check_anchor(str(ANCHORED_FIXTURE))
        self.assertTrue(result["ok"])
        self.assertTrue(result["anchor_present"])
        self.assertEqual(result["anchor_file"], "ANCHOR_SEPOLIA.json")
        self.assertEqual(result["anchor_data"]["chain"], "sepolia")
        self.assertEqual(result["verification_scope"], "metadata_presence_only")
        self.assertFalse(result["on_chain_verification_performed"])

    def test_summary_keeps_demo_status_visible(self) -> None:
        result = summarize_bundle(str(VALID_BUNDLE))
        self.assertTrue(result["ok"])
        self.assertTrue(result["status"]["is_demo"])
        self.assertTrue(result["status"]["passes_basic_verification"])

    def test_missing_source_returns_structured_failure(self) -> None:
        result = verify_bundle(str(REPOSITORY_ROOT / "demo" / "missing.zip"))
        self.assertFalse(result["valid"])
        self.assertTrue(any("load_error" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
