"""Utility functions for the functional analysis agent."""

from __future__ import annotations

import os

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


def get_message_text(msg: BaseMessage) -> str:
    """Extract plain text content from a message.

    This mirrors the helper used in the base react_agent template so that we can
    robustly handle different message content structures.
    """

    content = msg.content
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        return content.get("text", "")

    # Assume it is a list of parts
    parts: list[str] = []
    for c in content:
        if isinstance(c, str):
            parts.append(c)
        else:
            text = c.get("text") if isinstance(c, dict) else None
            if text:
                parts.append(text)
    return "".join(parts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    The name must be of the form ``provider/model``.

    We route OpenAI, DeepSeek (via an OpenAI-compatible endpoint), and
    XIAO_AI (via an OpenAI-compatible endpoint) through
    ``langchain-openai``'s ``init_chat_model`` helper by specifying the
    ``model_provider`` argument as the provider.

    For DeepSeek we rely on its OpenAI-compatible API. When the model name
    contains "deepseek", we temporarily map ``DEEPSEEK_API_KEY`` /
    ``DEEPSEEK_BASE_URL`` onto ``OPENAI_API_KEY`` / ``OPENAI_BASE_URL`` so
    that ``langchain-openai``'s ``ChatOpenAI`` client can talk to that
    endpoint without changing the rest of the code.

    For XIAO_AI we similarly rely on its OpenAI-compatible API. When the
    model name starts with "gpt-5", we temporarily map ``XIAOAI_API_KEY`` /
    ``XIAOAI_BASE_URL`` (default base ``https://xiaoai.plus/v1``) onto
    ``OPENAI_API_KEY`` / ``OPENAI_BASE_URL``.
    """

    provider, model = fully_specified_name.split("/", maxsplit=1)

    # For DeepSeek, temporarily override OPENAI_* env vars so that the
    # OpenAI-compatible client can talk to their endpoint without impacting
    # subsequent calls that target OpenAI directly.
    if "deepseek" in model:
        api_key_env = "DEEPSEEK_API_KEY"
        base_env = "DEEPSEEK_BASE_URL"
        default_base = "https://api.deepseek.com/v1"

        custom_key = os.getenv(api_key_env)
        custom_base = os.getenv(base_env, default_base)

        orig_key = os.getenv("OPENAI_API_KEY")
        orig_base = os.getenv("OPENAI_BASE_URL")

        if custom_key:
            os.environ["OPENAI_API_KEY"] = custom_key
        if custom_base:
            os.environ["OPENAI_BASE_URL"] = custom_base

        try:
            return init_chat_model(model, model_provider=provider)
        finally:
            if orig_key is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = orig_key

            if orig_base is None:
                os.environ.pop("OPENAI_BASE_URL", None)
            else:
                os.environ["OPENAI_BASE_URL"] = orig_base

    # For XIAO_AI (gpt-5), temporarily override OPENAI_* env vars so that the
    # OpenAI-compatible client can talk to the XIAO_AI endpoint.
    if model.startswith("gpt-5"):
        api_key_env = "XIAOAI_API_KEY"
        base_env = "XIAOAI_BASE_URL"
        default_base = "https://xiaoai.plus/v1"

        custom_key = os.getenv(api_key_env)
        custom_base = os.getenv(base_env, default_base)

        orig_key = os.getenv("OPENAI_API_KEY")
        orig_base = os.getenv("OPENAI_BASE_URL")

        if custom_key:
            os.environ["OPENAI_API_KEY"] = custom_key
        if custom_base:
            os.environ["OPENAI_BASE_URL"] = custom_base

        try:
            return init_chat_model(model, model_provider=provider)
        finally:
            if orig_key is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = orig_key

            if orig_base is None:
                os.environ.pop("OPENAI_BASE_URL", None)
            else:
                os.environ["OPENAI_BASE_URL"] = orig_base

    return init_chat_model(model, model_provider=provider)
