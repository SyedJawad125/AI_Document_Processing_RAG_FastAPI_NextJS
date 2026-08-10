# Import all models here so Alembic autogenerate detects them
from app.models.user import (
    Company, Role, Permission, User, Employee, UserToken,
    UserType, EmployeeStatus, SubscriptionPlan,
)
from app.models.document import (
    Document, DocumentPage, DocumentChunk,
    DocumentStatus, ExtractionMethod,
)

__all__ = [
    'Company', 'Role', 'Permission', 'User', 'Employee', 'UserToken',
    'UserType', 'EmployeeStatus', 'SubscriptionPlan',
    'Document', 'DocumentPage', 'DocumentChunk',
    'DocumentStatus', 'ExtractionMethod',
]