"""Application configuration — single source of truth for env vars."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    env: str = "development"
    log_level: str = "INFO"

    database_url: str
    redis_url: str = "redis://localhost:6379/0"

    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_app_name: str = "sharpz-analytics"
    openrouter_http_referer: str = "https://sharpzanalytics.com"

    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket_stimulus: str = "sharpz-stimulus"
    r2_bucket_deliverables: str = "sharpz-deliverables"

    sharpz_sync_key: str = ""
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_deliverable_expiry_days: int = 90

    resend_api_key: str = ""
    email_from: str = "noreply@sharpzanalytics.com"

    enable_local_ner: bool = False
    enable_local_embeddings: bool = False
    enable_multi_seed_aggregation: bool = True

    tier_economy_cost_cap_usd: float = 25.0
    tier_pro_cost_cap_usd: float = 60.0
    tier_premium_cost_cap_usd: float = 120.0
    tier_ultra_cost_cap_usd: float = 300.0

    cors_allowed_origins: str = "https://sharpzanalytics.com"
    operator_notification_email: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.env == "production"


settings = Settings()  # type: ignore[call-arg]  # values come from env
