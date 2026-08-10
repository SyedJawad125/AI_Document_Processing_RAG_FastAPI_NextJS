"""
app/services/llm_service.py
────────────────────────────
Groq LLM integration — used by RAG, summary, and extraction services.

Why Groq?
  - Fastest inference available (GroqChip hardware)
  - Free tier with generous limits
  - OpenAI-compatible API
  - llama-3.1-8b-instant: fast and capable for document Q&A

Pattern:
  - All LLM calls go through this service
  - Centralized retry logic (tenacity)
  - Centralized error handling
  - Structured JSON output for extraction
"""

import json
import logging
from typing import Optional

from groq import Groq, APITimeoutError, APIError
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.exceptions import LLMError, LLMTimeoutError

logger = logging.getLogger(__name__)


class LLMService:
    """Singleton Groq LLM client."""

    def __init__(self):
        self._client = Groq(
            api_key=settings.GROQ_API_KEY,
            timeout=settings.GROQ_TIMEOUT,
        )
        self.model = settings.GROQ_MODEL

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def complete(
        self,
        system_prompt:  str,
        user_prompt:    str,
        temperature:    float = 0.1,
        max_tokens:     int   = 2000,
        json_mode:      bool  = False,
    ) -> str:
        """
        Send a chat completion request to Groq.
        Returns the response text.
        """
        try:
            kwargs = dict(
                model    = self.model,
                messages = [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user',   'content': user_prompt},
                ],
                temperature = temperature,
                max_tokens  = max_tokens,
            )
            if json_mode:
                kwargs['response_format'] = {'type': 'json_object'}

            response    = self._client.chat.completions.create(**kwargs)
            result_text = response.choices[0].message.content
            tokens      = response.usage.total_tokens

            logger.info(f'[LLM] {self.model} — {tokens} tokens used')
            return result_text

        except APITimeoutError:
            logger.error('[LLM] Request timed out')
            raise LLMTimeoutError()
        except APIError as e:
            logger.error(f'[LLM] Groq API error: {e}')
            raise LLMError(f'Groq API error: {str(e)}')

    async def complete_json(
        self,
        system_prompt: str,
        user_prompt:   str,
        temperature:   float = 0.0,
        max_tokens:    int   = 2000,
    ) -> dict:
        """
        Send a request and parse the response as JSON.
        Groq's JSON mode guarantees valid JSON output.
        """
        text = await self.complete(
            system_prompt = system_prompt,
            user_prompt   = user_prompt,
            temperature   = temperature,
            max_tokens    = max_tokens,
            json_mode     = True,
        )
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f'[LLM] JSON parse failed: {e}\nText: {text[:200]}')
            raise LLMError(f'LLM returned invalid JSON: {str(e)}')

    # ── RAG Q&A ────────────────────────────────────────────────────

    async def answer_from_context(
        self,
        question: str,
        context:  str,
        filename: str = 'document',
    ) -> str:
        """
        Generate an answer grounded strictly in the provided context.
        LLM is instructed not to invent information.
        """
        system = (
            'You are a precise document analysis assistant. '
            'Answer ONLY from the provided document context. '
            'If the answer is not in the context, say exactly: '
            '"I could not find this information in the provided document." '
            'Include page citations like [Page 12] when page numbers are available. '
            'Never invent or assume information not present in the context.'
        )
        user = (
            f'Document: {filename}\n\n'
            f'Context from document:\n{context}\n\n'
            f'Question: {question}\n\n'
            'Answer:'
        )
        return await self.complete(system, user, temperature=0.1, max_tokens=1500)

    # ── Summarization ──────────────────────────────────────────────

    async def summarize_chunks(self, chunks_text: str) -> str:
        """Summarize a batch of chunks (used in hierarchical summarization)."""
        system = (
            'You are a document summarization expert. '
            'Create a concise, accurate summary of the provided text. '
            'Preserve all key facts, numbers, dates, and names.'
        )
        user = f'Summarize this document section:\n\n{chunks_text}'
        return await self.complete(system, user, temperature=0.2, max_tokens=800)

    async def final_summary(self, combined_summaries: str, filename: str) -> dict:
        """Generate structured final summary from chunk summaries."""
        system = (
            'You are a senior document analyst. '
            'Create a structured executive summary. '
            'Return valid JSON only — no markdown, no extra text.'
        )
        user = (
            f'Document: {filename}\n\n'
            f'Section summaries:\n{combined_summaries}\n\n'
            'Return JSON with exactly these keys:\n'
            '{\n'
            '  "executive_summary": "2-3 paragraph overview",\n'
            '  "key_points": ["point 1", "point 2", "..."],\n'
            '  "important_facts": ["fact 1", "fact 2", "..."],\n'
            '  "important_numbers": ["$14.2M revenue", "350 employees", "..."],\n'
            '  "risks": ["risk 1", "risk 2"],\n'
            '  "conclusion": "1 paragraph conclusion"\n'
            '}'
        )
        return await self.complete_json(system, user, temperature=0.2, max_tokens=2000)

    # ── Structured Extraction ──────────────────────────────────────

    async def extract_fields(self, fields: list[str], context: str, filename: str) -> dict:
        """
        Extract specific fields from document context.
        Returns structured JSON with status per field.
        """
        fields_str = '\n'.join(f'- {f}' for f in fields)
        system = (
            'You are a precise data extraction specialist. '
            'Extract ONLY information explicitly stated in the context. '
            'Return valid JSON only. '
            'For each field, return: {"value": <value or null>, "status": "found|not_found|uncertain"}. '
            'NEVER invent or guess values. If uncertain, use status: "uncertain".'
        )
        user = (
            f'Document: {filename}\n\n'
            f'Context:\n{context}\n\n'
            f'Extract these fields:\n{fields_str}\n\n'
            'Return JSON where each field name maps to {"value": ..., "status": "found|not_found|uncertain"}.'
        )
        return await self.complete_json(system, user, temperature=0.0, max_tokens=1500)


# Singleton instance
llm_service = LLMService()