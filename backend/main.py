"""
app/main.py
────────────
FastAPI application entry point.

What happens here:
  1. App created with metadata (shows in Swagger UI)
  2. CORS middleware configured
  3. Global exception handlers registered
  4. All API routers mounted under /api/v1/
  5. Startup/shutdown events for DB connection pooling
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import structlog

from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.api.v1 import auth, documents, search, chat, extraction, reports, users


# ─────────────────────────────────────────────────────────────────
#  Startup / Shutdown
# ─────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs once on startup and once on shutdown."""
    # ── Startup ───────────────────────────────────────────────────
    logging.basicConfig(level=settings.LOG_LEVEL)
    logger = logging.getLogger('app')
    logger.info(f'Starting {settings.APP_NAME} [{settings.ENVIRONMENT}]')

    # Create upload/report directories if they don't exist
    import os
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.REPORT_DIR, exist_ok=True)
    logger.info(f'Upload dir: {settings.UPLOAD_DIR} | Report dir: {settings.REPORT_DIR}')

    yield

    # ── Shutdown ──────────────────────────────────────────────────
    from app.db.database import engine
    await engine.dispose()
    logger.info('Database connections closed.')


# ─────────────────────────────────────────────────────────────────
#  FastAPI App
# ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title       = settings.APP_NAME,
    description = (
        'AI-powered document processing system. '
        'Upload PDFs → RAG Q&A → AI summaries → Structured extraction → PDF reports.'
    ),
    version     = '1.0.0',
    docs_url    = '/api/docs',
    redoc_url   = '/api/redoc',
    openapi_url = '/api/openapi.json',
    lifespan    = lifespan,
)


# ─────────────────────────────────────────────────────────────────
#  Middleware
# ─────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins     = settings.allowed_origins,
    allow_credentials = True,
    allow_methods     = ['*'],
    allow_headers     = ['*'],
)


# ─────────────────────────────────────────────────────────────────
#  Exception Handlers
# ─────────────────────────────────────────────────────────────────

register_exception_handlers(app)


# ─────────────────────────────────────────────────────────────────
#  Routers
# ─────────────────────────────────────────────────────────────────

PREFIX = '/api/v1'

app.include_router(auth.router,       prefix=f'{PREFIX}/auth',       tags=['Authentication'])
app.include_router(users.router,      prefix=f'{PREFIX}/users',      tags=['Users & Roles'])
app.include_router(documents.router,  prefix=f'{PREFIX}/documents',  tags=['Documents'])
app.include_router(search.router,     prefix=f'{PREFIX}/search',     tags=['Search'])
app.include_router(chat.router,       prefix=f'{PREFIX}/chat',       tags=['Chat / RAG'])
app.include_router(extraction.router, prefix=f'{PREFIX}/extraction', tags=['Extraction'])
app.include_router(reports.router,    prefix=f'{PREFIX}/reports',    tags=['Reports'])


# ─────────────────────────────────────────────────────────────────
#  Health Check
# ─────────────────────────────────────────────────────────────────

@app.get('/health', tags=['Health'])
async def health_check():
    return {
        'status':  'healthy',
        'app':     settings.APP_NAME,
        'version': '1.0.0',
        'env':     settings.ENVIRONMENT,
    }