"""Tools used by the functional analysis agent.

Currently this exposes a single retrieval tool backed by the PDF index.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, cast

from langgraph.runtime import get_runtime

from functional_analysis_agent.context import Context
from functional_analysis_agent.index import (
    RetrievedChunk,
    TheoryChunk,
    load_index,
    load_theories_index,
)


async def retrieve_from_materials(query: str) -> Optional[dict[str, Any]]:
    """Retrieve relevant snippets from the functional analysis PDF.

    This tool is used by the agent as the RAG component: given a question,
    intermediate step, or formula, it returns a small set of related text
    chunks from the course material.
    """

    runtime = get_runtime(Context)
    top_k = int(getattr(runtime.context, "rag_top_k", 5))

    index = load_index()
    chunks: list[RetrievedChunk] = index.search(query, top_k=top_k)

    return cast(
        dict[str, Any],
        {
            "query": query,
            "results": [
                {"text": c.text, "page": c.page} for c in chunks
            ],
        },
    )


async def retrieve_from_theories(query: str) -> Optional[dict[str, Any]]:
    """Retrieve relevant theorems from the theories.md summary file."""

    runtime = get_runtime(Context)
    top_k = int(getattr(runtime.context, "rag_top_k", 5))

    index = load_theories_index()
    chunks: list[TheoryChunk] = index.search(query, top_k=top_k)

    return cast(
        dict[str, Any],
        {
            "query": query,
            "results": [
                {"text": c.text, "label": c.label} for c in chunks
            ],
        },
    )


TOOLS: List[Callable[..., Any]] = [retrieve_from_materials, retrieve_from_theories]
