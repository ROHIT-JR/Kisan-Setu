"""Environment configuration. All external-cost knobs live here so the ₹0 constraint is enforced in one place."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "development"
    version: str = "0.1.0"

    # Never point this at a Pro model — Pro left the Gemini free tier in April 2026.
    gemini_model: str = "gemini-flash-latest"
    gemini_api_key: str = ""
    mock_gemini: bool = True
    max_gemini_calls_per_day: int = 800

    gcp_project_id: str = "kisan-setu-hackathon"
    gcp_region: str = "us-central1"

    earth_engine_service_account: str = ""
    earth_engine_key_path: str = ""

    firestore_enabled: bool = False

    cors_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
