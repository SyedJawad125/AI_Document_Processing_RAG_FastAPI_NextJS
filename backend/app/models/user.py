# """
# app/models/user.py
# ───────────────────
# SQLAlchemy ORM models matching your Django users app.

# Models:
#   Company    → multi-tenant (all documents scoped to a company)
#   Role       → group of permissions
#   Permission → single action (e.g. can_upload_documents)
#   User       → the main auth entity
#   Employee   → HR profile linked to a User
#   UserToken  → device tokens for push notifications / refresh

# Why a separate Company model?
#   - Multi-tenancy: each company's documents are isolated
#   - Supports SaaS — multiple companies on one instance
#   - Subscription plan controls feature limits
# """

# import uuid
# from datetime import datetime
# from enum import Enum as PyEnum

# from sqlalchemy import (
#     Boolean, Column, DateTime, ForeignKey,
#     Integer, String, Text, Enum, Table, func,
# )
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import relationship

# from app.db.database import Base


# # ─────────────────────────────────────────────────────────────────
# #  Enums
# # ─────────────────────────────────────────────────────────────────

# class UserType(str, PyEnum):
#     CUSTOMER = 'customer'
#     EMPLOYEE = 'employee'
#     ADMIN    = 'admin'


# class EmployeeStatus(str, PyEnum):
#     INVITED     = 'invited'
#     ACTIVE      = 'active'
#     DEACTIVATED = 'deactivated'


# class SubscriptionPlan(str, PyEnum):
#     FREE         = 'free'
#     STARTER      = 'starter'
#     PROFESSIONAL = 'professional'
#     ENTERPRISE   = 'enterprise'


# # ─────────────────────────────────────────────────────────────────
# #  Association table — Role ↔ Permission (many-to-many)
# # ─────────────────────────────────────────────────────────────────

# role_permissions = Table(
#     'role_permissions',
#     Base.metadata,
#     Column('role_id',       UUID(as_uuid=True), ForeignKey('roles.id',       ondelete='CASCADE'), primary_key=True),
#     Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
# )


# # ─────────────────────────────────────────────────────────────────
# #  TimeStampMixin — reusable created_at / updated_at
# # ─────────────────────────────────────────────────────────────────

# class TimeStampMixin:
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
#     updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
#     deleted    = Column(Boolean, default=False, nullable=False)


# # ─────────────────────────────────────────────────────────────────
# #  Company
# # ─────────────────────────────────────────────────────────────────

# class Company(TimeStampMixin, Base):
#     __tablename__ = 'companies'

#     id   = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String(255), unique=True, nullable=False, index=True)
#     slug = Column(String(255), unique=True, nullable=False, index=True)

#     email       = Column(String(255), nullable=True)
#     phone       = Column(String(30), nullable=True)
#     address     = Column(String(500), nullable=True)
#     website     = Column(String(255), nullable=True)
#     description = Column(Text, nullable=True)
#     logo        = Column(String(500), nullable=True)

#     subscription_plan       = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
#     monthly_screening_limit = Column(Integer, default=50, nullable=False)
#     is_active               = Column(Boolean, default=True, nullable=False)

#     # Relationships
#     users     = relationship('User',     back_populates='company', lazy='selectin')
#     documents = relationship('Document', back_populates='company', lazy='selectin')

#     def __repr__(self):
#         return f'<Company {self.name}>'


# # ─────────────────────────────────────────────────────────────────
# #  Permission
# # ─────────────────────────────────────────────────────────────────

# class Permission(Base):
#     __tablename__ = 'permissions'

#     id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name         = Column(String(100), nullable=False)
#     code_name    = Column(String(100), unique=True, nullable=False, index=True)
#     module_name  = Column(String(100), nullable=False)
#     module_label = Column(String(100), nullable=True)
#     description  = Column(String(255), nullable=False, default='')
#     created_at   = Column(DateTime(timezone=True), server_default=func.now())

#     # Relationships
#     roles = relationship('Role', secondary=role_permissions, back_populates='permissions')

#     def __repr__(self):
#         return f'<Permission {self.code_name}>'


# # ─────────────────────────────────────────────────────────────────
# #  Role
# # ─────────────────────────────────────────────────────────────────

# class Role(TimeStampMixin, Base):
#     __tablename__ = 'roles'

#     id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name        = Column(String(100), nullable=False)
#     code_name   = Column(String(50), unique=True, nullable=False, index=True)
#     description = Column(String(250), nullable=False, default='')

#     # Relationships
#     permissions = relationship('Permission', secondary=role_permissions, back_populates='roles', lazy='selectin')
#     users       = relationship('User', back_populates='role')

#     def __repr__(self):
#         return f'<Role {self.name}>'

#     def has_permission(self, code_name: str) -> bool:
#         return any(p.code_name == code_name for p in self.permissions)


# # ─────────────────────────────────────────────────────────────────
# #  User
# # ─────────────────────────────────────────────────────────────────

# class User(TimeStampMixin, Base):
#     __tablename__ = 'users'

#     id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     username   = Column(String(100), unique=True, nullable=False, index=True)
#     email      = Column(String(255), unique=True, nullable=False, index=True)
#     first_name = Column(String(100), nullable=False)
#     last_name  = Column(String(100), nullable=False)
#     full_name  = Column(String(200), nullable=True)
#     mobile     = Column(String(35), nullable=True)

#     password_hash    = Column(String(255), nullable=True)
#     profile_image    = Column(String(500), nullable=True)

#     is_active    = Column(Boolean, default=False, nullable=False)
#     is_verified  = Column(Boolean, default=False, nullable=False)
#     is_staff     = Column(Boolean, default=False, nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_blocked   = Column(Boolean, default=False, nullable=False)
#     deactivated  = Column(Boolean, default=False, nullable=False)
#     login_attempts = Column(Integer, default=0, nullable=False)

#     type = Column(Enum(UserType), default=UserType.CUSTOMER, nullable=False)

#     # Password reset (OTP-based)
#     password_reset_code            = Column(String(6),   nullable=True)
#     password_reset_code_created_at = Column(DateTime(timezone=True), nullable=True)
#     password_reset_verified        = Column(Boolean, default=False)

#     # Legacy link-based reset
#     password_link_token            = Column(String(255), nullable=True)
#     password_link_token_created_at = Column(DateTime(timezone=True), nullable=True)

#     # Activation
#     activation_link_token            = Column(String(255), nullable=True)
#     activation_link_token_created_at = Column(DateTime(timezone=True), nullable=True)

#     last_password_changed = Column(DateTime(timezone=True), nullable=True)
#     last_login            = Column(DateTime(timezone=True), nullable=True)
#     address               = Column(String(255), nullable=True)

#     # Foreign keys
#     role_id    = Column(UUID(as_uuid=True), ForeignKey('roles.id',     ondelete='SET NULL'), nullable=True)
#     company_id = Column(UUID(as_uuid=True), ForeignKey('companies.id', ondelete='SET NULL'), nullable=True)

#     # Relationships
#     role     = relationship('Role',    back_populates='users',    lazy='selectin')
#     company  = relationship('Company', back_populates='users',    lazy='selectin')
#     employee = relationship('Employee', back_populates='user',    uselist=False)
#     tokens   = relationship('UserToken', back_populates='user',   cascade='all, delete-orphan')
#     documents = relationship('Document', back_populates='owner',  lazy='selectin')

#     def __repr__(self):
#         return f'<User {self.email}>'

#     def has_perm(self, code_name: str) -> bool:
#         """Check if user's role has the given permission."""
#         if self.is_superuser:
#             return True
#         if not self.role:
#             return False
#         return self.role.has_permission(code_name)

#     @property
#     def display_name(self) -> str:
#         return self.full_name or f'{self.first_name} {self.last_name}'


# # ─────────────────────────────────────────────────────────────────
# #  Employee
# # ─────────────────────────────────────────────────────────────────

# class Employee(TimeStampMixin, Base):
#     __tablename__ = 'employees'

#     id      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True, unique=True)
#     status  = Column(Enum(EmployeeStatus), default=EmployeeStatus.INVITED, nullable=False)

#     # Relationships
#     user = relationship('User', back_populates='employee')

#     def __repr__(self):
#         return f'<Employee user_id={self.user_id} status={self.status}>'


# # ─────────────────────────────────────────────────────────────────
# #  UserToken  (device/refresh tokens)
# # ─────────────────────────────────────────────────────────────────

# class UserToken(Base):
#     __tablename__ = 'user_tokens'

#     id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id      = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
#     device_token = Column(Text, nullable=True)
#     token_hash   = Column(String(255), nullable=True, index=True)    # hashed refresh token
#     created_at   = Column(DateTime(timezone=True), server_default=func.now())
#     expires_at   = Column(DateTime(timezone=True), nullable=True)
#     is_revoked   = Column(Boolean, default=False)

#     # Relationships
#     user = relationship('User', back_populates='tokens')




"""
app/models/user.py
──────────────────
SQLAlchemy ORM models matching your Django users app.

Models:
    Company    → multi-tenant company
    Role       → group of permissions
    Permission → single permission/action
    User       → main authentication entity
    Employee   → HR profile linked to User
    UserToken  → device/refresh tokens
"""

from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Enum,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base

from app.models.mixins import (
    UUIDMixin,
    TimeStampMixin,
    SoftDeleteMixin,
    BaseModelMixin,
)
from app.models.associations import role_permissions

# ═════════════════════════════════════════════════════════════════════
# Enums
# ═════════════════════════════════════════════════════════════════════


class UserType(str, PyEnum):
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    ADMIN = "admin"


class EmployeeStatus(str, PyEnum):
    INVITED = "invited"
    ACTIVE = "active"
    DEACTIVATED = "deactivated"


class SubscriptionPlan(str, PyEnum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"



# ═════════════════════════════════════════════════════════════════════
# Company
# ═════════════════════════════════════════════════════════════════════


class Company(BaseModelMixin, Base):
    __tablename__ = "companies"

    name = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    slug = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String(255),
        nullable=True,
    )

    phone = Column(
        String(30),
        nullable=True,
    )

    address = Column(
        String(500),
        nullable=True,
    )

    website = Column(
        String(255),
        nullable=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    logo = Column(
        String(500),
        nullable=True,
    )

    subscription_plan = Column(
        Enum(SubscriptionPlan),
        default=SubscriptionPlan.FREE,
        nullable=False,
    )

    monthly_screening_limit = Column(
        Integer,
        default=50,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships

    users = relationship(
        "User",
        back_populates="company",
        lazy="selectin",
    )

    documents = relationship(
        "Document",
        back_populates="company",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Company {self.name}>"


# ═════════════════════════════════════════════════════════════════════
# Permission
# ═════════════════════════════════════════════════════════════════════


class Permission(UUIDMixin, Base):
    __tablename__ = "permissions"

    name = Column(
        String(100),
        nullable=False,
    )

    code_name = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    module_name = Column(
        String(100),
        nullable=False,
    )

    module_label = Column(
        String(100),
        nullable=True,
    )

    description = Column(
        String(255),
        nullable=False,
        default="",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships

    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions",
    )

    def __repr__(self):
        return f"<Permission {self.code_name}>"


# ═════════════════════════════════════════════════════════════════════
# Role
# ═════════════════════════════════════════════════════════════════════


class Role(BaseModelMixin, Base):
    __tablename__ = "roles"

    name = Column(
        String(100),
        nullable=False,
    )

    code_name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    description = Column(
        String(250),
        nullable=False,
        default="",
    )

    # Relationships

    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
        lazy="selectin",
    )

    users = relationship(
        "User",
        back_populates="role",
    )

    def __repr__(self):
        return f"<Role {self.name}>"

    def has_permission(self, code_name: str) -> bool:
        return any(
            permission.code_name == code_name
            for permission in self.permissions
        )


# ═════════════════════════════════════════════════════════════════════
# User
# ═════════════════════════════════════════════════════════════════════


class User(UUIDMixin, TimeStampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name = Column(
        String(100),
        nullable=False,
    )

    last_name = Column(
        String(100),
        nullable=False,
    )

    full_name = Column(
        String(200),
        nullable=True,
    )

    mobile = Column(
        String(35),
        nullable=True,
    )

    # Authentication

    password_hash = Column(
        String(255),
        nullable=True,
    )

    profile_image = Column(
        String(500),
        nullable=True,
    )

    # Account status

    is_active = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_staff = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_blocked = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    deactivated = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    login_attempts = Column(
        Integer,
        default=0,
        nullable=False,
    )

    type = Column(
        Enum(UserType),
        default=UserType.CUSTOMER,
        nullable=False,
    )

    # Password reset - OTP based

    password_reset_code = Column(
        String(6),
        nullable=True,
    )

    password_reset_code_created_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    password_reset_verified = Column(
        Boolean,
        default=False,
    )

    # Legacy link-based password reset

    password_link_token = Column(
        String(255),
        nullable=True,
    )

    password_link_token_created_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Account activation

    activation_link_token = Column(
        String(255),
        nullable=True,
    )

    activation_link_token_created_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Login / password information

    last_password_changed = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    last_login = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    address = Column(
        String(255),
        nullable=True,
    )

    # Foreign keys

    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "roles.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    company_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "companies.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    # Relationships

    role = relationship(
        "Role",
        back_populates="users",
        lazy="selectin",
    )

    company = relationship(
        "Company",
        back_populates="users",
        lazy="selectin",
    )

    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
    )

    tokens = relationship(
        "UserToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    documents = relationship(
        "Document",
        back_populates="owner",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<User {self.email}>"

    def has_perm(self, code_name: str) -> bool:
        """
        Check if user's role has the given permission.
        Superusers automatically have every permission.
        """

        if self.is_superuser:
            return True

        if not self.role:
            return False

        return self.role.has_permission(code_name)

    @property
    def display_name(self) -> str:
        return self.full_name or f"{self.first_name} {self.last_name}"


# ═════════════════════════════════════════════════════════════════════
# Employee
# ═════════════════════════════════════════════════════════════════════


class Employee(BaseModelMixin, Base):
    __tablename__ = "employees"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        unique=True,
    )

    status = Column(
        Enum(EmployeeStatus),
        default=EmployeeStatus.INVITED,
        nullable=False,
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="employee",
    )

    def __repr__(self):
        return (
            f"<Employee "
            f"user_id={self.user_id} "
            f"status={self.status}>"
        )


# ═════════════════════════════════════════════════════════════════════
# UserToken
# ═════════════════════════════════════════════════════════════════════


class UserToken(UUIDMixin, Base):
    __tablename__ = "user_tokens"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    device_token = Column(
        Text,
        nullable=True,
    )

    token_hash = Column(
        String(255),
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_revoked = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Relationships

    user = relationship(
        "User",
        back_populates="tokens",
    )