"""
app/models/mixins.py
─────────────────────
Reusable SQLAlchemy mixins shared across all models.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TimeStampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)


class SoftDeleteMixin:
    deleted = Column(Boolean, default=False, nullable=False)


class BaseModelMixin(UUIDMixin, TimeStampMixin, SoftDeleteMixin):
    """Full mixin: UUID pk + timestamps + soft delete."""
    pass