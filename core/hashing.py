"""
hashing.py
SHA-256 utilities for HREVN bundle verification.
"""

import hashlib


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_str(text: str, encoding: str = "utf-8") -> str:
    return sha256_bytes(text.encode(encoding))


def compute_root_hash(
    files: dict[str, bytes],
    root_scope: list[str],
    serialization: dict,
) -> str:
    """
    Recompute the root hash following ROOT_SPEC_AER_V1 rules.
    serialization keys used: encoding, line_separator, sort_order, trailing_newline
    """
    encoding = serialization.get("encoding", "utf-8")
    line_sep = serialization.get("line_separator", "\\n").replace("\\n", "\n")
    trailing = serialization.get("trailing_newline", False)

    scope_files = sorted(root_scope)  # ascending filename, as per spec
    pairs = []
    for fname in scope_files:
        if fname not in files:
            raise KeyError(f"root_scope file not found in bundle: {fname}")
        h = sha256_bytes(files[fname])
        pairs.append(f"{fname}:{h}")

    serialized = line_sep.join(pairs)
    if trailing:
        serialized += line_sep

    return sha256_str(serialized, encoding)
