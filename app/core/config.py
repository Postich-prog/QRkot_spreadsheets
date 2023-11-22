from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "QRKot"
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    email = "EMAIL"
    type: str = "TYPE"
    project_id: str = "PROJECT_ID"
    private_key_id: str = "PRIVATE_KEY_ID"
    private_key: str = "PRIVATE_KEY"
    client_email: str = "CLIENT_EMAIL"
    client_id: int = "CLIENT_ID"
    auth_uri: str = "AUTH_URI"
    token_uri: str = "TOKEN_URI"
    auth_provider_x509_cert_url = "AUTH_PROVIDER_X509_CERT_URL"
    client_x509_cert_url = "CLIENT_X509_CERT_URL"
    universe_domain = "UNIVERSE_DOMAIN"

    class Config:
        env_file = ".env"


settings = Settings()
