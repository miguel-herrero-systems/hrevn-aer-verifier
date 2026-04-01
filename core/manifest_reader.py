"""
manifest_reader.py
Parse and expose fields from manifest.json.
"""

import json
from dataclasses import dataclass, field


class ManifestError(Exception):
    pass


@dataclass
class Manifest:
    raw: dict

    # identity
    aer_id: str = ""
    record_id: str = ""
    workflow_id: str = ""
    bundle_profile: str = ""
    package_type: str = ""
    package_family: str = ""
    version: str = ""
    generated_at_utc: str = ""

    # structure
    artifact_count: int = 0
    artifacts: list = field(default_factory=list)
    root_scope: list = field(default_factory=list)
    checksum_scope: list = field(default_factory=list)
    authoritative_files: list = field(default_factory=list)
    supporting_files: list = field(default_factory=list)

    # verification
    verification_model: str = ""
    root_serialization: dict = field(default_factory=dict)
    signature_status: str = ""
    external_anchor_status: str = ""


def parse_manifest(data: bytes) -> Manifest:
    try:
        raw = json.loads(data.decode("utf-8"))
    except Exception as e:
        raise ManifestError(f"Cannot parse manifest.json: {e}")

    m = Manifest(raw=raw)
    m.aer_id = raw.get("aer_id", "")
    m.record_id = raw.get("record_id", "")
    m.workflow_id = raw.get("workflow_id", "")
    m.bundle_profile = raw.get("bundle_profile", "")
    m.package_type = raw.get("package_type", "")
    m.package_family = raw.get("package_family", "")
    m.version = raw.get("version", "")
    m.generated_at_utc = raw.get("generated_at_utc", "")
    m.artifact_count = raw.get("artifact_count", 0)
    m.artifacts = raw.get("artifacts", [])
    m.root_scope = raw.get("root_scope", [])
    m.checksum_scope = raw.get("checksum_scope", [])
    m.authoritative_files = raw.get("authoritative_files", [])
    m.supporting_files = raw.get("supporting_files", [])
    m.verification_model = raw.get("verification_model", "")
    m.root_serialization = raw.get("root_serialization", {})
    m.signature_status = raw.get("signature_status", "")
    m.external_anchor_status = raw.get("external_anchor_status", "")
    return m
