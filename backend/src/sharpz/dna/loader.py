"""Load DNAs from the `dna/` directory at repo root and cache in memory.

DNAs are YAML files validated against a loose schema. Full schema
validation (pydantic model of the DNA structure) is a m2 concern —
for m1 we keep it permissive and validate only required keys needed
by Stage 1 (intake validation).
"""

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

# Resolve repo root from this file: backend/src/sharpz/dna/loader.py → up 4
_REPO_ROOT = Path(__file__).resolve().parents[4]
_DNA_DIR = _REPO_ROOT / "dna"


class DNALoadError(Exception):
    """Raised when a DNA file is missing or malformed."""


_REQUIRED_TOP_LEVEL_KEYS = (
    "test_type",
    "version",
    "status",
    "panel",
    "simulation",
    "stimulus",
    "metrics",
    "report",
)


def _validate_minimal(dna: dict[str, Any], source: Path) -> None:
    missing = [k for k in _REQUIRED_TOP_LEVEL_KEYS if k not in dna]
    if missing:
        raise DNALoadError(f"{source.name} missing required keys: {missing}")

    status = dna.get("status")
    if status not in {"active", "deprecated", "experimental"}:
        raise DNALoadError(f"{source.name} has invalid status: {status!r}")


@lru_cache(maxsize=1)
def load_all_dnas() -> dict[str, dict[str, Any]]:
    """Read every `*.yaml` in `dna/` and return a dict keyed by test_type.

    Cached — restart process to pick up changes (or call load_all_dnas.cache_clear()).
    """
    if not _DNA_DIR.is_dir():
        raise DNALoadError(f"dna/ directory not found at {_DNA_DIR}")

    dnas: dict[str, dict[str, Any]] = {}
    for yaml_path in sorted(_DNA_DIR.glob("*.yaml")):
        with yaml_path.open(encoding="utf-8") as f:
            dna = yaml.safe_load(f)
        if not isinstance(dna, dict):
            raise DNALoadError(f"{yaml_path.name} did not parse to a mapping")
        _validate_minimal(dna, yaml_path)

        test_type = dna["test_type"]
        if test_type in dnas:
            raise DNALoadError(f"duplicate test_type {test_type!r} in {yaml_path.name}")
        dnas[test_type] = dna

    return dnas


def get_dna(test_type: str) -> dict[str, Any]:
    """Return the DNA for a test_type, or raise DNALoadError."""
    dnas = load_all_dnas()
    if test_type not in dnas:
        raise DNALoadError(f"unknown test_type: {test_type!r}")
    return dnas[test_type]


def list_active_test_types() -> list[str]:
    """Returns test_type IDs with status == 'active'."""
    return [tt for tt, dna in load_all_dnas().items() if dna.get("status") == "active"]
