"""
app/services/llm_service.py
────────────────────────────
UPDATED: Rewritten using LangChain LCEL chains.

Before: direct Groq SDK calls
After:  LangChain ChatGroq + PromptTemplate + OutputParser chains

Why LCEL (LangChain Expression Language)?
  chain = prompt | llm | parser
  - Composable: add steps by chaining with |
  - Streamable: swap .invoke() for .stream() with zero changes
  - Observable: LangSmith tracing works automatically
  - Testable: mock any step independently
  - Fallback: chain.with_fallbacks([backup_llm])
"""

import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.langchain_setup import llm, summary_llm, json_llm
from app.core.config import settings
from app.core.exceptions import LLMError, LLMTimeoutError

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────
#  RAG Q&A Chain
# ─────────────────────────────────────────────────────────────────

RAG_SYSTEM = """You are a precise document analysis assistant.
Answer ONLY from the provided document context.
If the answer is not in the context, say exactly:
"I could not find this information in the provided document."
Include page citations like [Page 12] when page numbers are available.
Never invent or assume information not present in the context."""

rag_prompt = ChatPromptTemplate.from_messages([
    ('system', RAG_SYSTEM),
    ('human', 'Document: {filename}\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:'),
])

# LCEL chain: prompt → LLM → string output
rag_chain = rag_prompt | llm | StrOutputParser()


# ─────────────────────────────────────────────────────────────────
#  Document Grading Chain  (NEW — used by LangGraph agent)
# ─────────────────────────────────────────────────────────────────

GRADING_SYSTEM = """You are a relevance grader for a document retrieval system.
Given a user question and a retrieved document chunk, determine if the chunk
is relevant to answering the question.

Return JSON only:
{{"relevant": true/false, "reason": "brief explanation", "score": 0.0-1.0}}"""

grading_prompt = ChatPromptTemplate.from_messages([
    ('system', GRADING_SYSTEM),
    ('human', 'Question: {question}\n\nChunk:\n{chunk}'),
])

grading_chain = grading_prompt | json_llm | JsonOutputParser()


# ─────────────────────────────────────────────────────────────────
#  Query Rewriting Chain  (NEW — used by LangGraph agent)
# ─────────────────────────────────────────────────────────────────

REWRITE_SYSTEM = """You are a query optimisation expert for document search.
Rewrite the user's question to be more specific and searchable.
Make it better for vector similarity search.
Return only the rewritten query — no explanation."""

rewrite_prompt = ChatPromptTemplate.from_messages([
    ('system', REWRITE_SYSTEM),
    ('human', 'Original question: {question}\n\nRewritten query:'),
])

rewrite_chain = rewrite_prompt | llm | StrOutputParser()


# ─────────────────────────────────────────────────────────────────
#  Summarisation Chain
# ─────────────────────────────────────────────────────────────────

CHUNK_SUMMARY_SYSTEM = """You are a document summarisation expert.
Create a concise, accurate summary preserving all key facts, numbers, dates, and names."""

chunk_summary_prompt = ChatPromptTemplate.from_messages([
    ('system', CHUNK_SUMMARY_SYSTEM),
    ('human', 'Summarise this section:\n\n{text}'),
])

chunk_summary_chain = chunk_summary_prompt | summary_llm | StrOutputParser()


FINAL_SUMMARY_SYSTEM = """You are a senior document analyst.
Create a structured executive summary. Return valid JSON only."""

FINAL_SUMMARY_TEMPLATE = """Document: {filename}

Section summaries:
{combined_summaries}

Return JSON with exactly these keys:
{{
  "executive_summary": "2-3 paragraph overview",
  "key_points": ["point 1", "point 2"],
  "important_facts": ["fact 1", "fact 2"],
  "important_numbers": ["$14.2M revenue", "350 employees"],
  "risks": ["risk 1"],
  "conclusion": "1 paragraph conclusion"
}}"""

final_summary_prompt = ChatPromptTemplate.from_messages([
    ('system', FINAL_SUMMARY_SYSTEM),
    ('human', FINAL_SUMMARY_TEMPLATE),
])

final_summary_chain = final_summary_prompt | json_llm | JsonOutputParser()


# ─────────────────────────────────────────────────────────────────
#  Extraction Chain
# ─────────────────────────────────────────────────────────────────

EXTRACTION_SYSTEM = """You are a precise data extraction specialist.
Extract ONLY information explicitly stated in the context.
For each field return: {{"value": <value or null>, "status": "found|not_found|uncertain"}}
NEVER invent or guess values."""

EXTRACTION_TEMPLATE = """Document: {filename}

Context:
{context}

Extract these fields:
{fields}

Return JSON where each field maps to {{"value": ..., "status": "found|not_found|uncertain"}}."""

extraction_prompt = ChatPromptTemplate.from_messages([
    ('system', EXTRACTION_SYSTEM),
    ('human', EXTRACTION_TEMPLATE),
])

extraction_chain = extraction_prompt | json_llm | JsonOutputParser()


# ─────────────────────────────────────────────────────────────────
#  LLMService — thin wrapper calling LCEL chains
# ─────────────────────────────────────────────────────────────────

class LLMService:
    """
    Thin service layer over LCEL chains.
    All methods are async and use .ainvoke() for non-blocking calls.
    """

    @property
    def model(self) -> str:
        return settings.GROQ_MODEL

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def answer_from_context(self, question: str, context: str, filename: str) -> str:
        """RAG Q&A — answer grounded in retrieved context."""
        try:
            result = await rag_chain.ainvoke({
                'question': question,
                'context':  context,
                'filename': filename,
            })
            logger.info(f'[LLM] RAG answer generated — {len(result)} chars')
            return result
        except Exception as e:
            logger.error(f'[LLM] answer_from_context failed: {e}')
            raise LLMError(str(e))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def grade_document(self, question: str, chunk: str) -> dict:
        """Grade whether a chunk is relevant to the question (used by agent)."""
        try:
            return await grading_chain.ainvoke({'question': question, 'chunk': chunk})
        except Exception as e:
            logger.warning(f'[LLM] grading failed: {e}')
            return {'relevant': True, 'score': 0.5, 'reason': 'grading unavailable'}

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(min=1, max=5))
    async def rewrite_query(self, question: str) -> str:
        """Rewrite query to improve retrieval (used by agent)."""
        try:
            return await rewrite_chain.ainvoke({'question': question})
        except Exception as e:
            logger.warning(f'[LLM] query rewrite failed: {e}')
            return question   # fallback to original

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def summarize_chunks(self, chunks_text: str) -> str:
        try:
            if summary_llm is None:
                logger.error('[LLM] summary_llm is None - check GROQ_API_KEY')
                raise LLMError('LLM not initialized. Check GROQ_API_KEY in .env')
            return await chunk_summary_chain.ainvoke({'text': chunks_text})
        except Exception as e:
            logger.error(f'[LLM] summarize_chunks error: {e}')
            raise LLMError(str(e))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def final_summary(self, combined_summaries: str, filename: str) -> dict:
        try:
            if json_llm is None:
                logger.error('[LLM] json_llm is None - check GROQ_API_KEY')
                raise LLMError('LLM not initialized. Check GROQ_API_KEY in .env')
            return await final_summary_chain.ainvoke({
                'combined_summaries': combined_summaries,
                'filename':           filename,
            })
        except Exception as e:
            logger.error(f'[LLM] final_summary error: {e}')
            raise LLMError(str(e))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def extract_fields(self, fields: list[str], context: str, filename: str) -> dict:
        try:
            return await extraction_chain.ainvoke({
                'fields':   '\n'.join(f'- {f}' for f in fields),
                'context':  context,
                'filename': filename,
            })
        except Exception as e:
            raise LLMError(str(e))


llm_service = LLMService()