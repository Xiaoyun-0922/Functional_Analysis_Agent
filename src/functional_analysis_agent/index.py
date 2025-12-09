"""PDF indexing and retrieval utilities for the functional analysis agent.

This module builds and loads a simple vector index over the course material
PDF located in ``functional_analysis_materials/functional_analysis.pdf``.

We use OpenAI embeddings (via langchain) plus a NumPy-based in-memory index,
optionally persisted to disk for faster reuse.
"""

from __future__ import annotations

import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

import numpy as np
from dotenv import dotenv_values
from langchain_openai import OpenAIEmbeddings
from pypdf import PdfReader


@dataclass
class RetrievedChunk:
    """A single retrieved text chunk from the PDF."""

    text: str
    page: int


@dataclass
class PdfIndex:
    """Simple in-memory vector index over PDF chunks."""

    embeddings: np.ndarray
    texts: List[str]
    pages: List[int]

    def search(self, query: str, top_k: int = 5) -> List[RetrievedChunk]:
        """Return top_k most similar chunks for the given query."""

        if not len(self.texts):
            return []

        embedder = _make_embedder()
        if embedder is None:
            return []
        q_vec = np.array(embedder.embed_query(query), dtype="float32")

        # Normalize embeddings and query to compute cosine similarity
        doc_vecs = self.embeddings
        q_norm = np.linalg.norm(q_vec) + 1e-8
        d_norms = np.linalg.norm(doc_vecs, axis=1) + 1e-8
        sims = (doc_vecs @ q_vec) / (d_norms * q_norm)

        top_k = min(top_k, len(self.texts))
        idxs = np.argsort(-sims)[:top_k]

        return [
            RetrievedChunk(text=self.texts[i], page=self.pages[i]) for i in idxs
        ]


@dataclass
class TheoryChunk:
    """A single retrieved theorem/proposition chunk from theories.md."""

    text: str
    label: str


@dataclass
class TheoryIndex:
    """Simple in-memory vector index over theorem summary chunks."""

    embeddings: np.ndarray
    texts: List[str]
    labels: List[str]

    def search(self, query: str, top_k: int = 5) -> List[TheoryChunk]:
        """Return top_k most similar theorem chunks for the given query."""

        if not len(self.texts):
            return []

        embedder = _make_embedder()
        if embedder is None:
            return []
        q_vec = np.array(embedder.embed_query(query), dtype="float32")

        # Normalize embeddings and query to compute cosine similarity
        doc_vecs = self.embeddings
        q_norm = np.linalg.norm(q_vec) + 1e-8
        d_norms = np.linalg.norm(doc_vecs, axis=1) + 1e-8
        sims = (doc_vecs @ q_vec) / (d_norms * q_norm)

        top_k = min(top_k, len(self.texts))
        idxs = np.argsort(-sims)[:top_k]

        return [
            TheoryChunk(text=self.texts[i], label=self.labels[i]) for i in idxs
        ]


def _project_root() -> Path:
    """Return the project root assuming this file is under src/functional_analysis_agent."""

    here = Path(__file__).resolve()
    return here.parents[2]


def _ensure_embedding_env() -> None:
    """Ensure OPENAI_API_KEY is set in os.environ for embeddings.

    We first trust any existing environment variable. If it is missing,
    we fall back to reading the project's .env file explicitly.
    """

    if os.getenv("OPENAI_API_KEY"):
        return

    env_path = _project_root() / ".env"
    if not env_path.exists():
        return

    values = dotenv_values(str(env_path))
    key = values.get("OPENAI_API_KEY") if values is not None else None
    if key:
        os.environ["OPENAI_API_KEY"] = str(key)


_ensure_embedding_env()


def _get_openai_api_key() -> str | None:
    """Return OPENAI_API_KEY from environment or .env, if available.

    Resolution order:
    1. Existing process environment (OPENAI_API_KEY already exported).
    2. .env in the current working directory (where uvicorn/uv is run).
    3. .env in the computed project root (two levels above this file).
    """

    # 1. Directly from existing environment variables.
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key

    # 2. Try .env in the current working directory.
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        values = dotenv_values(str(cwd_env))
        key = values.get("OPENAI_API_KEY") if values is not None else None
        if key:
            return str(key)

    # 3. Fall back to .env in the computed project root.
    env_path = _project_root() / ".env"
    if env_path.exists():
        values = dotenv_values(str(env_path))
        key = values.get("OPENAI_API_KEY") if values is not None else None
        if key:
            return str(key)

    return None


def _make_embedder() -> OpenAIEmbeddings | None:
    """Create an OpenAIEmbeddings instance backed by a resolved API key.

    This helper ensures the OPENAI_API_KEY environment variable is set so that
    langchain-openai / openai can always see a configured api_key.
    Returns ``None`` if no key can be resolved.
    """

    key = _get_openai_api_key()
    if not key:
        return None

    os.environ["OPENAI_API_KEY"] = str(key)
    return OpenAIEmbeddings()


def _pdf_path() -> Path:
    return _project_root() / "functional_analysis_materials" / "functional_analysis.pdf"


def _index_path() -> Path:
    return _project_root() / "data" / "functional_analysis_index.pkl"


def _theories_path() -> Path:
    return _project_root() / "data" / "theories.md"


def _theories_index_path() -> Path:
    return _project_root() / "data" / "theories_index.pkl"


def build_index(chunk_size: int = 800, chunk_overlap: int = 200) -> PdfIndex:
    """Build a fresh index from the functional analysis PDF.

    This reads the PDF, splits pages into overlapping text chunks, computes
    OpenAI embeddings for each chunk, and saves the resulting index to disk.
    """

    pdf_file = _pdf_path()
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF not found at {pdf_file}")

    reader = PdfReader(str(pdf_file))
    texts: List[str] = []
    pages: List[int] = []

    for page_num, page in enumerate(reader.pages):
        raw_text = (page.extract_text() or "").strip()
        if not raw_text:
            continue

        # Simple sliding window chunking by characters
        start = 0
        while start < len(raw_text):
            end = min(start + chunk_size, len(raw_text))
            chunk = raw_text[start:end].strip()
            if chunk:
                texts.append(chunk)
                pages.append(page_num + 1)
            if end == len(raw_text):
                break
            start = end - chunk_overlap

    if not texts:
        raise ValueError("No text extracted from PDF; check the file contents.")

    embedder = _make_embedder()
    if embedder is None:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured; cannot build PDF embeddings index."
        )
    vectors = embedder.embed_documents(texts)
    emb_array = np.asarray(vectors, dtype="float32")

    index = PdfIndex(embeddings=emb_array, texts=texts, pages=pages)

    index_file = _index_path()
    index_file.parent.mkdir(parents=True, exist_ok=True)
    with index_file.open("wb") as f:
        pickle.dump(index, f)

    return index


def load_index() -> PdfIndex:
    """Load the existing index, or build it if it does not yet exist."""

    index_file = _index_path()
    if index_file.exists():
        with index_file.open("rb") as f:
            index = pickle.load(f)
        if not isinstance(index, PdfIndex):
            raise TypeError("Loaded index object has unexpected type")
        return index

    return build_index()


def _parse_theories_md(path: Path) -> tuple[List[str], List[str]]:
    """Parse theories.md into text chunks and human-readable labels."""

    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    texts: List[str] = []
    labels: List[str] = []

    current_block: List[str] = []
    current_label_parts: List[str] = []
    current_chapter = ""
    current_section = ""

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## ") and not stripped.startswith("###"):
            # Chapter-level header, e.g. "## 第一章 距离空间"
            current_chapter = stripped[3:].strip()
            current_section = ""
            continue

        if stripped.startswith("### ") and not stripped.startswith("####"):
            # Section-level header, e.g. "### §1.3 距离空间的完备性"
            current_section = stripped[4:].strip()
            continue

        if stripped.startswith("#### "):
            # Start of a new theorem/lemma/proposition block.
            if current_block:
                text = "\n".join(current_block).strip()
                if text:
                    label = " / ".join(p for p in current_label_parts if p)
                    labels.append(label or "unnamed")
                    texts.append(text)
                current_block = []

            title = stripped[5:].strip()
            parts: List[str] = []
            if current_chapter:
                parts.append(current_chapter)
            if current_section:
                parts.append(current_section)
            parts.append(title)
            current_label_parts = parts
            current_block.append(stripped)
            continue

        if current_block:
            current_block.append(line)

    if current_block:
        text = "\n".join(current_block).strip()
        if text:
            label = " / ".join(p for p in current_label_parts if p)
            labels.append(label or "unnamed")
            texts.append(text)

    return texts, labels


def build_theories_index() -> TheoryIndex:
    """Build a fresh index from the theorem summary file theories.md."""

    theories_file = _theories_path()
    if not theories_file.exists():
        raise FileNotFoundError(f"Theories file not found at {theories_file}")

    texts, labels = _parse_theories_md(theories_file)
    if not texts:
        raise ValueError("No theorem chunks parsed from theories.md")

    embedder = _make_embedder()
    if embedder is None:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured; cannot build theories embeddings index."
        )
    vectors = embedder.embed_documents(texts)
    emb_array = np.asarray(vectors, dtype="float32")

    index = TheoryIndex(embeddings=emb_array, texts=texts, labels=labels)

    index_file = _theories_index_path()
    index_file.parent.mkdir(parents=True, exist_ok=True)
    with index_file.open("wb") as f:
        pickle.dump(index, f)

    return index


def load_theories_index() -> TheoryIndex:
    """Load the existing theories index, or build it if it does not exist."""

    index_file = _theories_index_path()
    if index_file.exists():
        with index_file.open("rb") as f:
            index = pickle.load(f)
        if not isinstance(index, TheoryIndex):
            raise TypeError("Loaded theories index object has unexpected type")
        return index

    return build_theories_index()
