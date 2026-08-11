"""
app/services/rag_service.py
────────────────────────────
Full RAG (Retrieval-Augmented Generation) pipeline.

Flow:
  Question → Embed → Vector Search → Top-K Chunks
  → Build Context → Groq LLM → Answer + Citations

Why RAG?
  - LLM only answers from retrieved document content
  - No hallucinations about content not in the document
  - Page citations are grounded in actual retrieved chunks
  - Works for ANY document without fine-tuning
"""

import logging
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.vector_search_service import vector_search_service, SearchResult
from app.services.llm_service import llm_service
from app.repositories.document_repository import DocumentRepository
from app.core.exceptions import NotFoundError, ValidationError

logger = logging.getLogger(__name__)


@dataclass
class Citation:
    chunk_id:    str
    document_id: str
    filename:    str
    page_number: Optional[int]


@dataclass
class RAGResponse:
    question:  str
    answer:    str
    citations: list[Citation]
    model:     str
    chunks_used: int


class RAGService:

    async def answer(
        self,
        question:    str,
        document_id: str,
        db:          AsyncSession,
        top_k:       int = 5,
    ) -> RAGResponse:
        """
        Main RAG pipeline: question → answer + citations.

        Steps:
          1. Verify document is ready
          2. Search for relevant chunks
          3. Build context from chunks
          4. Call Groq LLM with context
          5. Return answer + chunk citations
        """
        # 1. Load document
        doc_repo = DocumentRepository(db)
        document = await doc_repo.get_by_id(document_id)
        if not document:
            raise NotFoundError('Document')
        if not document.is_ready:
            raise ValidationError(f'Document is not ready yet. Current status: {document.status}')

        # 2. Retrieve relevant chunks
        results = await vector_search_service.search(
            query       = question,
            document_id = document_id,
            db          = db,
            top_k       = top_k,
        )

        # 3. If no results found — inform user
        if not results:
            return RAGResponse(
                question    = question,
                answer      = 'I could not find this information in the provided document.',
                citations   = [],
                model       = llm_service.model,
                chunks_used = 0,
            )

        # 4. Build context with page references
        context = vector_search_service.build_context(results)

        # 5. Generate answer
        answer = await llm_service.answer_from_context(
            question = question,
            context  = context,
            filename = document.original_filename,
        )

        # 6. Build citations from retrieved chunks
        citations = [
            Citation(
                chunk_id    = r.chunk_id,
                document_id = r.document_id,
                filename    = document.original_filename,
                page_number = r.page_number,
            )
            for r in results
        ]

        logger.info(
            f'[RAG] Question answered | doc={document_id} | '
            f'chunks={len(results)} | answer_len={len(answer)}'
        )

        return RAGResponse(
            question    = question,
            answer      = answer,
            citations   = citations,
            model       = llm_service.model,
            chunks_used = len(results),
        )


rag_service = RAGService()