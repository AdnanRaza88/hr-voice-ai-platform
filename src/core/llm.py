from functools import lru_cache
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from src.core.config import ProviderName, get_settings, reload_settings


def build_chat_model(
    provider: ProviderName | None = None,
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> BaseChatModel:
    settings = get_settings()
    provider = provider or settings.llm_provider

    if provider == "groq":
        from langchain_groq import ChatGroq

        api_key = settings.groq_api_key
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured")
        return ChatGroq(
            api_key=api_key,
            model_name=model or settings.groq_model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        api_key = settings.openai_api_key
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        return ChatOpenAI(
            api_key=api_key,
            model=model or settings.openai_model,
            base_url=settings.openai_base_url or None,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    if provider == "opencode_zen":
        from langchain_openai import ChatOpenAI

        api_key = settings.opencode_api_key
        if not api_key:
            raise RuntimeError("OPENCODE_API_KEY is not configured")
        return ChatOpenAI(
            api_key=api_key,
            model=model or settings.opencode_model,
            base_url=settings.opencode_base_url,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=model or settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=temperature,
        )

    raise RuntimeError(f"Unsupported provider: {provider}")


def provider_status() -> dict[str, Any]:
    settings = get_settings()
    return {
        "active": settings.llm_provider,
        "providers": {
            "groq": {
                "configured": bool(settings.groq_api_key),
                "model": settings.groq_model,
            },
            "openai": {
                "configured": bool(settings.openai_api_key),
                "model": settings.openai_model,
                "base_url": settings.openai_base_url,
            },
            "opencode_zen": {
                "configured": bool(settings.opencode_api_key),
                "model": settings.opencode_model,
                "base_url": settings.opencode_base_url,
            },
            "ollama": {
                "configured": True,
                "model": settings.ollama_model,
                "base_url": settings.ollama_base_url,
            },
        },
    }


def apply_provider_config(data: dict[str, Any]) -> dict[str, Any]:
    env_path = get_settings().base_dir / ".env"
    lines: list[str] = []
    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines()

    def set_key(key: str, value: str) -> None:
        nonlocal lines
        prefix = f"{key}="
        found = False
        new_lines: list[str] = []
        for line in lines:
            if line.startswith(prefix) or line.startswith(f"# {prefix}"):
                new_lines.append(f"{key}={value}")
                found = True
            else:
                new_lines.append(line)
        if not found:
            new_lines.append(f"{key}={value}")
        lines = new_lines

    if "llm_provider" in data and data["llm_provider"]:
        set_key("LLM_PROVIDER", str(data["llm_provider"]))
    if "groq_api_key" in data and data["groq_api_key"] is not None:
        set_key("GROQ_API_KEY", str(data["groq_api_key"]))
    if "groq_model" in data and data["groq_model"]:
        set_key("GROQ_MODEL", str(data["groq_model"]))
    if "openai_api_key" in data and data["openai_api_key"] is not None:
        set_key("OPENAI_API_KEY", str(data["openai_api_key"]))
    if "openai_model" in data and data["openai_model"]:
        set_key("OPENAI_MODEL", str(data["openai_model"]))
    if "opencode_api_key" in data and data["opencode_api_key"] is not None:
        set_key("OPENCODE_API_KEY", str(data["opencode_api_key"]))
    if "opencode_model" in data and data["opencode_model"]:
        set_key("OPENCODE_MODEL", str(data["opencode_model"]))
    if "ollama_model" in data and data["ollama_model"]:
        set_key("OLLAMA_MODEL", str(data["ollama_model"]))

    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    reload_settings()
    return provider_status()


@lru_cache
def get_default_llm() -> BaseChatModel:
    return build_chat_model()


def clear_llm_cache() -> None:
    get_default_llm.cache_clear()
