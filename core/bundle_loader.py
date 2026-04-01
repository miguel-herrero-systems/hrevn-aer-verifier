"""
bundle_loader.py
Loads an HREVN bundle from a ZIP file or a directory.
Returns a flat dict: {filename: bytes}
"""

import zipfile
from pathlib import Path


class BundleLoadError(Exception):
    pass


def load_bundle(source: str | Path) -> dict[str, bytes]:
    """
    Load all files from a bundle.
    source: path to .zip file OR path to extracted directory.
    Returns {filename: bytes} — filenames are bare (no directory prefix).
    """
    source = Path(source)

    if not source.exists():
        raise BundleLoadError(f"Source not found: {source}")

    if source.is_file() and source.suffix.lower() == ".zip":
        return _load_from_zip(source)
    elif source.is_dir():
        return _load_from_dir(source)
    else:
        raise BundleLoadError(f"Source must be a .zip file or a directory: {source}")


def _load_from_zip(path: Path) -> dict[str, bytes]:
    files = {}
    with zipfile.ZipFile(path, "r") as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = Path(info.filename).name  # strip any subfolder prefix
            files[name] = zf.read(info.filename)
    return files


def _load_from_dir(path: Path) -> dict[str, bytes]:
    files = {}
    for p in path.iterdir():
        if p.is_file():
            files[p.name] = p.read_bytes()
    return files
