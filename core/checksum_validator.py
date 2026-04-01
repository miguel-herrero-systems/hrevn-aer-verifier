"""
checksum_validator.py
Parse CHECKSUMS.sha256 and validate each file in the bundle.
"""

from .hashing import sha256_bytes


class ChecksumError(Exception):
    pass


def parse_checksums(data: bytes) -> dict[str, str]:
    """
    Parse CHECKSUMS.sha256 lines: '<hash>  <filename>'
    Returns {filename: expected_hash}
    """
    result = {}
    for line in data.decode("utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            raise ChecksumError(f"Malformed checksum line: {line!r}")
        h, fname = parts
        result[fname.strip()] = h.strip()
    return result


def validate_checksums(
    files: dict[str, bytes],
    expected: dict[str, str],
) -> dict:
    """
    Compare actual hashes against expected.
    Returns:
      {
        "valid": bool,
        "passed": [filenames],
        "failed": [{"file": ..., "expected": ..., "actual": ...}],
        "missing": [filenames not found in bundle],
        "unchecked": [filenames in bundle but not in checksum list],
      }
    """
    passed = []
    failed = []
    missing = []

    for fname, exp_hash in expected.items():
        if fname not in files:
            missing.append(fname)
            continue
        actual = sha256_bytes(files[fname])
        if actual == exp_hash:
            passed.append(fname)
        else:
            failed.append({"file": fname, "expected": exp_hash, "actual": actual})

    checked = set(expected.keys())
    unchecked = [f for f in files if f not in checked and f != "CHECKSUMS.sha256"]

    return {
        "valid": len(failed) == 0 and len(missing) == 0,
        "passed": passed,
        "failed": failed,
        "missing": missing,
        "unchecked": unchecked,
    }
