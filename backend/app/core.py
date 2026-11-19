"""Configuration and local filesystem paths."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    data_dir: Path = Path("./data")
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    max_upload_bytes: int = 10 * 1024 * 1024
    chunk_size: int = 1200
    chunk_overlap: int = 180

settings = Settings()
