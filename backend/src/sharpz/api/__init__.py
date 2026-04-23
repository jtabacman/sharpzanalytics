"""FastAPI routers."""

from sharpz.api.intakes import router as intakes_router
from sharpz.api.operator import router as operator_router

__all__ = ["intakes_router", "operator_router"]
