#!/usr/bin/env python3
"""
HREVN AER Verifier Plugin — CLI entrypoint
Usage: python main.py <tool> source=<path>

Tools:
  verify_bundle     Full integrity verification
  inspect_manifest  Read manifest metadata
  list_evidence     List all artifacts with hashes
  check_anchor      Check for external anchor
  summarize_bundle  Executive summary (recommended first call)

Example:
  python main.py summarize_bundle source=/path/to/bundle.zip
  python main.py verify_bundle source=/path/to/bundle/
"""

import sys
import json

from tools import (
    verify_bundle,
    inspect_manifest,
    list_evidence,
    check_anchor,
    summarize_bundle,
)

TOOLS = {
    "verify_bundle": verify_bundle,
    "inspect_manifest": inspect_manifest,
    "list_evidence": list_evidence,
    "check_anchor": check_anchor,
    "summarize_bundle": summarize_bundle,
}


def parse_args(argv):
    """Parse: <tool> source=<path> [key=value ...]"""
    if len(argv) < 3:
        return None, {}
    tool = argv[1]
    kwargs = {}
    for arg in argv[2:]:
        if "=" in arg:
            k, v = arg.split("=", 1)
            kwargs[k.strip()] = v.strip()
    return tool, kwargs


def main():
    tool_name, kwargs = parse_args(sys.argv)

    if tool_name is None or tool_name not in TOOLS:
        print(json.dumps({
            "error": "unknown_tool",
            "available_tools": list(TOOLS.keys()),
            "usage": "python main.py <tool> source=<path>",
        }, indent=2))
        sys.exit(1)

    source = kwargs.get("source", ".")
    result = TOOLS[tool_name](source)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
