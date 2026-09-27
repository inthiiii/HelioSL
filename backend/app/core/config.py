from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HelioSL API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = True

    api_v1_prefix: str = "/api/v1"

    database_url: str

    frontend_origin: str = "http://localhost:3000"

    secret_key: str
    access_token_expire_minutes: int = 60
    jwt_algorithm: str = "HS256"
    
    # LLM Configuration
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2"
    ollama_base_url: str = "http://127.0.0.1:11434"
    llm_timeout_seconds: int = 60
    llm_temperature: float = 0.2
    
    # RAG / Embedding Configuraiton
    embedding_model: str = "nomic-embed-text"
    rag_top_k: int = 5
    rag_chunk_size: int = 800
    rag_chunk_overlap: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
