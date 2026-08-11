"""
app/services/chunking_service.py
──────────────────────────────────
Intelligent text chunking for RAG.

Why chunk?
  - LLMs have context window limits
  - Smaller chunks = more precise retrieval
  - Overlap prevents cutting mid-sentence

Strategy:
  1. Split on sentence boundaries (not arbitrary character count)
  2. Accumulate sentences until chunk_size reached
  3. Overlap: carry last N words into next chunk
  4. Preserve page metadata per chunk

Config (from .env):
  CHUNK_SIZE    = 800  (target words per chunk)
  CHUNK_OVERLAP = 150  (words of overlap between chunks)
"""

import re
import logging
from dataclasses import dataclass

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    chunk_index: int
    content:     str
    page_number: int
    token_count: int
    metadata:    dict


class ChunkingService:

    def __init__(
        self,
        chunk_size:    int = None,
        chunk_overlap: int = None,
    ):
        self.chunk_size    = chunk_size    or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    def chunk_document(
        self,
        pages: list[dict],   # [{'page_number': 1, 'text': '...'}]
        document_id: str,
    ) -> list[Chunk]:
        """
        Chunk all pages of a document.
        Preserves page number metadata for citations.

        Returns list of Chunk objects ready for embedding.
        """
        all_chunks = []
        chunk_idx  = 0

        for page in pages:
            page_num = page['page_number']
            text     = page['text'].strip()

            if not text:
                continue

            page_chunks = self._chunk_text(text, page_num, chunk_idx, document_id)
            all_chunks.extend(page_chunks)
            chunk_idx += len(page_chunks)

        logger.info(f'[Chunking] Document {document_id}: {len(all_chunks)} chunks from {len(pages)} pages')
        return all_chunks

    def _chunk_text(
        self,
        text:        str,
        page_number: int,
        start_idx:   int,
        document_id: str,
    ) -> list[Chunk]:
        """
        Split a single page's text into overlapping chunks.

        Why sentence-based splitting?
          - Preserves semantic meaning
          - No mid-sentence cuts
          - Better retrieval quality
        """
        sentences = self._split_sentences(text)
        if not sentences:
            return []

        chunks      = []
        current     = []
        current_len = 0
        chunk_idx   = start_idx

        for sentence in sentences:
            words     = sentence.split()
            word_count = len(words)

            # If single sentence exceeds chunk_size, add it alone
            if word_count > self.chunk_size:
                if current:
                    chunks.append(self._make_chunk(current, chunk_idx, page_number, document_id))
                    chunk_idx += 1
                    current, current_len = [], 0

                # Split long sentence by hard limit
                for sub in self._hard_split(sentence):
                    chunks.append(self._make_chunk([sub], chunk_idx, page_number, document_id))
                    chunk_idx += 1
                continue

            if current_len + word_count > self.chunk_size and current:
                # Flush current chunk
                chunks.append(self._make_chunk(current, chunk_idx, page_number, document_id))
                chunk_idx += 1

                # Keep overlap: last N words carried into next chunk
                overlap_text = ' '.join(' '.join(current).split()[-self.chunk_overlap:])
                current      = [overlap_text] if overlap_text else []
                current_len  = len(overlap_text.split())

            current.append(sentence)
            current_len += word_count

        # Flush remaining
        if current:
            chunks.append(self._make_chunk(current, chunk_idx, page_number, document_id))

        return chunks

    def _make_chunk(
        self,
        sentences:   list[str],
        chunk_index: int,
        page_number: int,
        document_id: str,
    ) -> Chunk:
        content     = ' '.join(sentences).strip()
        word_count  = len(content.split())
        return Chunk(
            chunk_index = chunk_index,
            content     = content,
            page_number = page_number,
            token_count = word_count,
            metadata    = {
                'document_id': document_id,
                'page_number': page_number,
                'chunk_index': chunk_index,
            },
        )

    def _split_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences using regex.
        Handles: periods, exclamation marks, question marks.
        Avoids splitting on: Mr., Dr., abbreviations, decimals.
        """
        # Basic sentence splitter — handles most English text
        sentence_end = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
        sentences    = sentence_end.split(text)
        # Clean empty strings
        return [s.strip() for s in sentences if s.strip()]

    def _hard_split(self, text: str) -> list[str]:
        """Split oversized text by word count when no sentence boundary exists."""
        words  = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunk = ' '.join(words[i:i + self.chunk_size])
            chunks.append(chunk)
        return chunks


chunking_service = ChunkingService()