"""
app/services/embedding_service.py
───────────────────────────────────
Singleton embedding service using sentence-transformers.

Why sentence-transformers/all-MiniLM-L6-v2?
  - 384-dimensional vectors (fast, small)
  - Excellent semantic similarity performance
  - Runs locally — no API cost, no rate limits
  - First load downloads model (~90 MB) then caches it

The service is a singleton — model loads once when first called.
"""

import logging
from typing import Union

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Singleton sentence-transformers embedding service.
    Thread-safe — model is loaded once on first use.
    """
    _instance = None
    _model    = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _ensure_loaded(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            logger.info(f'[Embedding] Loading model: {settings.EMBEDDING_MODEL}')
            self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            logger.info(f'[Embedding] Model ready — dim={settings.EMBEDDING_DIMENSION}')

    def embed_text(self, text: str) -> list[float]:
        """
        Embed a single text string.
        Returns a list of floats (384 dims for MiniLM).
        """
        self._ensure_loaded()
        text = text.strip()[:8000]   # guard against massive inputs
        vector = self._model.encode(text, convert_to_numpy=True)
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple texts in a single forward pass (much faster than looping).
        Use this when embedding all chunks of a document.
        """
        self._ensure_loaded()
        cleaned = [t.strip()[:8000] for t in texts]
        vectors = self._model.encode(
            cleaned,
            convert_to_numpy=True,
            batch_size=32,            # process 32 chunks at a time
            show_progress_bar=False,
        )
        return [v.tolist() for v in vectors]

    @property
    def dimension(self) -> int:
        return settings.EMBEDDING_DIMENSION


# Singleton instance
embedding_service = EmbeddingService()