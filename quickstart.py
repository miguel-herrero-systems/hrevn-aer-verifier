#!/usr/bin/env python3
"""
HREVN AER Verifier — Quickstart Demo
=====================================
Run this to see the plugin in action against three demo bundles:

  python quickstart.py

No configuration needed. No external dependencies.
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from tools import verify_bundle, inspect_manifest, list_evidence, check_anchor, summarize_bundle

DEMO_DIR = os.path.join(os.path.dirname(__file__), "demo")

BUNDLES = [
    {
        "file": "CAR-2026-002_valid.zip",
        "label": "Bundle 1 — Valid AER (privileged access change)",
        "expect": "PASS",
    },
    {
        "file": "CAR-2026-002_tampered.zip",
        "label": "Bundle 2 — Tampered AER (operation_record modified)",
        "expect": "FAIL",
    },
    {
        "file": "CAR-2026-003_anchored.zip",
        "label": "Bundle 3 — Valid AER + Blockchain anchor (PII data export)",
        "expect": "PASS",
    },
]

GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def bar(char="─", n=60):
    print(char * n)


def print_header():
    print()
    bar("═")
    print(f"{BOLD}  HREVN AER Verifier — Quickstart Demo{RESET}")
    bar("═")
    print("  Three bundles. Three scenarios. Zero configuration.")
    bar("─")
    print()


def run_bundle(bundle_def):
    path = os.path.join(DEMO_DIR, bundle_def["file"])
    label = bundle_def["label"]
    expect = bundle_def["expect"]

    print(f"{BOLD}{CYAN}▶  {label}{RESET}")
    bar()

    # 1. Verify
    vr = verify_bundle(path)
    status = f"{GREEN}✔  VALID{RESET}" if vr["valid"] else f"{RED}✘  INVALID{RESET}"
    expected_ok = (vr["valid"] and expect == "PASS") or (not vr["valid"] and expect == "FAIL")
    expected_str = f"{GREEN}(expected){RESET}" if expected_ok else f"{RED}(unexpected!){RESET}"

    print(f"  Integrity:   {status}  {expected_str}")
    print(f"  Root hash:   {'match ✔' if vr.get('root_hash_match') else RED+'MISMATCH ✘'+RESET}")

    if vr["errors"]:
        for e in vr["errors"]:
            print(f"  {RED}  ✘ {e}{RESET}")

    if vr["warnings"]:
        for w in vr["warnings"]:
            print(f"  {YELLOW}  ⚠ {w}{RESET}")

    # 2. Identity from manifest
    im = inspect_manifest(path)
    if im["ok"]:
        print(f"  AER ID:      {im['aer_id']}")
        print(f"  Profile:     {im['bundle_profile']}")
        print(f"  Generated:   {im['generated_at_utc']}")

    # 3. Artifact summary
    le = list_evidence(path)
    if le["ok"]:
        cats = {}
        for a in le["artifacts"]:
            cats[a["category"]] = cats.get(a["category"], 0) + 1
        cat_str = "  |  ".join(f"{k}: {v}" for k, v in sorted(cats.items()))
        print(f"  Artifacts:   {le['total_files']} total  [{cat_str}]")

    # 4. Anchor
    ca = check_anchor(path)
    if ca["anchor_present"]:
        anchor_data = ca.get("anchor_data") or {}
        tx = anchor_data.get("tx_hash", "")
        chain = anchor_data.get("chain", "")
        print(f"  {GREEN}Anchor:      ⛓  {chain}  {tx[:20]}...{RESET}")
    else:
        print(f"  Anchor:      none")

    print()


def print_summary(results):
    bar("═")
    print(f"{BOLD}  Summary{RESET}")
    bar("─")
    for r in results:
        icon = f"{GREEN}✔{RESET}" if r["pass"] else f"{RED}✘{RESET}"
        print(f"  {icon}  {r['label']}")
    bar("═")
    print()
    print("  Next steps:")
    print("  • Run a specific tool:  python main.py verify_bundle source=demo/CAR-2026-002_valid.zip")
    print("  • Full JSON output:     python main.py summarize_bundle source=demo/CAR-2026-003_anchored.zip")
    print("  • Documentation:        README.md")
    print()


def main():
    print_header()
    results = []
    for bundle_def in BUNDLES:
        run_bundle(bundle_def)
        path = os.path.join(DEMO_DIR, bundle_def["file"])
        vr = verify_bundle(path)
        expected_ok = (vr["valid"] and bundle_def["expect"] == "PASS") or \
                      (not vr["valid"] and bundle_def["expect"] == "FAIL")
        results.append({"label": bundle_def["label"], "pass": expected_ok})
    print_summary(results)


if __name__ == "__main__":
    main()
