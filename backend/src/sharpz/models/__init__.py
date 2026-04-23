"""SQLModel table definitions — single source of truth for DB schema.

Alembic imports this package so SQLModel.metadata knows all tables.
Always import new model files here.
"""

from sharpz.models.enums import (
    ArchetypeRole,
    BrandAffinity,
    IntakeStatus,
    PriceSensitivity,
    TestStatus,
    Tier,
)
from sharpz.models.intake import Intake
from sharpz.models.test import Test

__all__ = [
    "ArchetypeRole",
    "BrandAffinity",
    "Intake",
    "IntakeStatus",
    "PriceSensitivity",
    "Test",
    "TestStatus",
    "Tier",
]
