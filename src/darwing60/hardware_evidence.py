"""Validate and summarize source-backed hardware research claims."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_PATH = REPOSITORY_ROOT / "devices" / "hanoip" / "hardware-evidence.json"
VALID_STATUSES = {"source_observed", "provisional", "unresolved"}
VALID_CONFIDENCE = {"high", "medium", "low", "unknown"}

class EvidenceError(ValueError):
    """Raised when the hardware evidence ledger is missing or malformed."""

def load_evidence(path: Path = EVIDENCE_PATH) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvidenceError(f"Evidence ledger not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"Invalid evidence JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise EvidenceError("Evidence ledger must be a JSON object.")
    return data

def validate_evidence(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("Unsupported evidence schema_version.")
    if data.get("device_codename") != "hanoip":
        errors.append("Evidence ledger must target hanoip.")
    claims = data.get("claims")
    if not isinstance(claims, list):
        return errors + ["claims must be a list."]
    seen: set[str] = set()
    for index, claim in enumerate(claims):
        prefix = f"Claim {index}"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(f"{prefix} needs a non-empty id.")
        elif claim_id in seen:
            errors.append(f"Duplicate claim id: {claim_id}.")
        else:
            seen.add(claim_id)
        for field in ("category", "subject", "finding"):
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                errors.append(f"{prefix} needs a non-empty {field}.")
        status = claim.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{prefix} has invalid status {status!r}.")
        if claim.get("confidence") not in VALID_CONFIDENCE:
            errors.append(f"{prefix} has invalid confidence.")
        sources = claim.get("sources")
        if not isinstance(sources, list):
            errors.append(f"{prefix} sources must be a list.")
            sources = []
        if status in {"source_observed", "provisional"} and not sources:
            errors.append(f"{prefix} needs at least one source for status {status}.")
        for source_index, source in enumerate(sources):
            if not isinstance(source, dict) or not isinstance(source.get("url"), str):
                errors.append(f"{prefix} source {source_index} needs a URL.")
            elif not source["url"].startswith(("https://", "http://")):
                errors.append(f"{prefix} source {source_index} URL must be HTTP(S).")
        if not isinstance(claim.get("limitations"), list):
            errors.append(f"{prefix} limitations must be a list.")
    return errors

def build_report(data: dict[str, Any] | None = None) -> str:
    """Render observations without promoting them to confirmed hardware facts."""
    ledger = data if data is not None else load_evidence()
    claims = ledger.get("claims", [])
    lines = [
        f"DarwinG60 hardware evidence: {ledger.get('device_codename', 'unknown')}",
        "Source observations only; not a physical hardware probe.",
        "",
    ]
    for claim in claims:
        lines.append(
            f"[{claim.get('status', 'unknown')}/{claim.get('confidence', 'unknown')}] "
            f"{claim.get('subject', claim.get('id', 'Unlabelled claim'))}"
        )
        lines.append(f"  {claim.get('finding', '')}")
        lines.append(f"  Sources: {len(claim.get('sources', []))}")
    unresolved = sum(1 for claim in claims if claim.get("status") == "unresolved")
    lines.extend(["", f"Unresolved claims: {unresolved}"])
    return "\\n".join(lines)
