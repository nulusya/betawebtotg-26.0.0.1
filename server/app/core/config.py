from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, SecretStr

class Settings(BaseSettings):
    PROJECT_NAME: str = "Telegram Shop SaaS"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: PostgresDsn
    
    # Security
    SHOPS_MASTER_KEY: SecretStr # 32 bytes hex or string for AES
    SECRET_KEY: SecretStr # For JWT
    
    # Bot
    WEBHOOK_BASE_URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
