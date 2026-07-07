from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, SecretStr, ValidationError

class Settings(BaseSettings):
    setu_client_id: SecretStr
    setu_client_secret: SecretStr
    setu_product_instance_id: SecretStr
    setu_base_url: AnyHttpUrl = "https://sandbox.setu.co/api"
    database_url: SecretStr
    redirect_url: AnyHttpUrl = "http://localhost:3000/status"
    app_secret: str = "change-me"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def validate_non_empty(self):
        for name, value in self:
            if isinstance(value, SecretStr) and not value.get_secret_value():
                raise ValueError(f"Missing required env var: {name}")

try:
    settings = Settings()
    settings.validate_non_empty()
except ValidationError as e:
    print(f"Config error: {e}")
    raise
