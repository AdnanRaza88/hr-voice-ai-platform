from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


ProviderName = Literal["groq", "openai", "opencode_zen", "ollama"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "HR Voice AI Agent"
    app_env: str = "development"
    debug: bool = True

    llm_provider: ProviderName = "groq"

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-70b-versatile"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    opencode_api_key: str = ""
    opencode_model: str = "big-pickle"
    opencode_base_url: str = "https://opencode.ai/zen/v1"

    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_persist_dir: str = "data/chroma"
    knowledge_dir: str = "data/knowledge"
    upload_dir: str = "data/uploads"

    chunk_size: int = 800
    chunk_overlap: int = 150
    retrieval_k: int = 4

    jwt_secret: str = "change-me-in-production-use-long-random-string"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def base_dir(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def chroma_path(self) -> Path:
        path = self.base_dir / self.chroma_persist_dir
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def knowledge_path(self) -> Path:
        path = self.base_dir / self.knowledge_dir
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def upload_path(self) -> Path:
        path = self.base_dir / self.upload_dir
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reload_settings() -> Settings:
    get_settings.cache_clear()
    return get_settings()
