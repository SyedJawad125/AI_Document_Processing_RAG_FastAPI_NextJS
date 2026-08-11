"""
app/services/embedding_service.py
───────────────────────────────────
UPDATED: Uses LangChain HuggingFaceEmbeddings wrapper.

Before: direct sentence_transformers.SentenceTransformer
After:  langchain_huggingface.HuggingFaceEmbeddings

Why the LangChain wrapper?
  - Same underlying sentence-transformers model
  - LangGraph tools expect LangChain Embeddings interface
  - normalize_embeddings=True → cosine similarity works correctly
  - Consistent with the rest of the LangChain stack
"""

import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Thin wrapper around LangChain HuggingFaceEmbeddings.
    Provides the same .embed_text() / .embed_batch() interface
    the rest of the codebase expects.
    """

    def __init__(self):
        # Lazy — model loads on first call
        self._lc_embeddings = None

    def _ensure_loaded(self):
        if self._lc_embeddings is None:
            # Import from our central setup — singleton guaranteed
            from app.core.langchain_setup import embeddings as lc_emb
            self._lc_embeddings = lc_emb
            logger.info(f'[Embedding] Ready — model: {settings.EMBEDDING_MODEL}')

    def embed_text(self, text: str) -> list[float]:
        """Embed a single string → list[float] (384 dims for MiniLM)."""
        self._ensure_loaded()
        text = text.strip()[:8000]
        return self._lc_embeddings.embed_query(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple strings — uses embed_documents() which
        LangChain batches internally for efficiency.
        """
        self._ensure_loaded()
        cleaned = [t.strip()[:8000] for t in texts]
        return self._lc_embeddings.embed_documents(cleaned)

    def get_langchain_embeddings(self):
        """Return the raw LangChain Embeddings object (used by agents)."""
        self._ensure_loaded()
        return self._lc_embeddings

    @property
    def dimension(self) -> int:
        return settings.EMBEDDING_DIMENSION


embedding_service = EmbeddingService()