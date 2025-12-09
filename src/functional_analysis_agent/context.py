"""Define the configurable parameters for the functional analysis agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated

from . import prompts


@dataclass(kw_only=True)
class Context:
    """Runtime context for the functional analysis agent.

    This context controls which model is used and how the RAG component behaves.
    """

    system_prompt: str = field(
        default=prompts.SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt for the agent's interactions. "
            "This sets the overall behavior and style of the tutor.",
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="openai/deepseek-chat",
        metadata={
            "description": (
                "Fully specified chat model name in the form 'provider/model'. "
                "Example: 'openai/deepseek-chat' when using DeepSeek via its "
                "OpenAI-compatible endpoint."
            )
        },
    )

    rag_top_k: int = field(
        default=5,
        metadata={
            "description": "Number of chunks to retrieve from the functional "
            "analysis PDF index for each query.",
        },
    )

    def __post_init__(self) -> None:
        """Fetch env vars for attributes that were not passed as args.

        For each init-able field, if its value is still the default, we look for
        an upper-case environment variable with the same name and use it if
        present. For example, MODEL or RAG_TOP_K.
        """

        for f in fields(self):
            if not f.init:
                continue

            current = getattr(self, f.name)
            if current == f.default:
                env_name = f.name.upper()
                setattr(self, f.name, os.environ.get(env_name, f.default))
