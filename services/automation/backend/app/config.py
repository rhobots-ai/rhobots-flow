from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import AliasChoices, Field

class Settings(BaseSettings):
    # App settings
    app_name: str = "AutomationStudio"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "4dc56f97778b03d1e25f79ca5dcdea8da7fe21b6d216e0787bba5c53d040f567"
    timezone: str = "America/New_York"
    
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://admin:password@postgres:5432/automation"
    
    # Storage settings
    STORAGE_BACKEND: str = "local"  # 'local' or 'minio'
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin123"
    MINIO_BUCKET_NAME: str = "automation-files"
    MINIO_PUBLIC_ENDPOINT: Optional[str] = None
    MINIO_REGION: str = "us-east-1"
    upload_dir: str = "/app/uploads"
    screenshot_dir: str = "/app/screenshots"
    max_upload_size: int = 10485760
    
    # VNC settings
    VNC_PUBLIC_HOST: str = "localhost"
    vnc_host: str = "vnc"
    vnc_display: str = ":1"
    vnc_port: int = 5901
    vnc_web_port: int = 7900
    
    # Playwright settings
    playwright_headless: bool = False
    playwright_timeout: int = 30000
    playwright_viewport_width: int = 1920
    playwright_viewport_height: int = 1080
    
    # WebSocket settings
    ws_heartbeat_interval: int = 30

    # Multi-session settings
    enable_multi_session: bool = Field(default=False, validation_alias=AliasChoices('enable_multi_session', 'ENABLE_MULTI_SESSION'))
    session_manager_url: str = Field(default="http://automation:8001", validation_alias=AliasChoices('session_manager_url', 'SESSION_MANAGER_URL'))

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
