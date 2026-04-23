"""Enums used across models — kept in one module to avoid circular imports."""

from enum import Enum


class IntakeStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class TestStatus(str, Enum):
    DRAFT = "draft"
    VALIDATED = "validated"
    PANEL_READY = "panel_ready"
    APPROVED_BY_OP = "approved_by_op"
    SIMULATING = "simulating"
    INTERVIEWING = "interviewing"
    SYNTHESIZING = "synthesizing"
    PUBLISHED = "published"
    COMPLETED = "completed"
    HALTED_ALERT = "halted_alert"
    HALTED_ABORT = "halted_abort"
    REFUNDED = "refunded"


class Tier(str, Enum):
    ECONOMY = "economy"
    PRO = "pro"
    PREMIUM = "premium"
    ULTRA = "ultra"


class BrandAffinity(str, Enum):
    ADVOCATE = "advocate"
    USER = "user"
    LAPSED = "lapsed"
    AWARE = "aware"
    UNAWARE = "unaware"


class PriceSensitivity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ArchetypeRole(str, Enum):
    HARDCORE = "hardcore"
    MAINSTREAM = "mainstream"
    SKEPTIC = "skeptic"
    ADVOCATE = "advocate"
    LAGGARD = "laggard"
    INFLUENCER = "influencer"
