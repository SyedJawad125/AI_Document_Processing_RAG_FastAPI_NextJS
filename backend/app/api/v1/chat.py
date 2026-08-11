"""
app/api/v1/chat.py
───────────────────
RAG-powered Q&A endpoint.

POST /api/v1/chat
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.rag_service import rag_service
from app.repositories.document_repository import DocumentRepository
from app.core.exceptions import NotFoundError, ValidationError
from app.utils.response import success_response

router = APIRouter()


@router.post('/')
async def chat_with_document(
    payload:      dict,
    current_user: User = Depends(get_current_user),
    db:           AsyncSession = Depends(get_db),
):
    """
    Ask a question about a document.
    Uses RAG: retrieve relevant chunks → Groq LLM → answer + citations.

    Request:
        { "document_id": "uuid", "question": "What was revenue in 2025?" }

    Response:
        { "answer": "...", "citations": [{"page_number": 12, ...}] }
    """
    document_id = payload.get('document_id', '').strip()
    question    = payload.get('question', '').strip()
    top_k       = int(payload.get('top_k', 5))

    if not document_id:
        raise ValidationError('document_id is required.')
    if not question:
        raise ValidationError('question is required.')

    # Verify ownership
    doc_repo = DocumentRepository(db)
    document = await doc_repo.get_by_id(document_id, user_id=current_user.id)
    if not document:
        raise NotFoundError('Document')

    response = await rag_service.answer(
        question    = question,
        document_id = document_id,
        db          = db,
        top_k       = top_k,
    )

    return success_response({
        'question': response.question,
        'answer':   response.answer,
        'model':    response.model,
        'chunks_used': response.chunks_used,
        'citations': [
            {
                'chunk_id':    c.chunk_id,
                'document_id': c.document_id,
                'filename':    c.filename,
                'page_number': c.page_number,
            }
            for c in response.citations
        ],
    })