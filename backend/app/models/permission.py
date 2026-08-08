# from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
# from sqlalchemy.orm import relationship
# from app.database import Base


# user_permission = Table(
#     "user_permission",
#     Base.metadata,
#     Column("user_id", Integer, ForeignKey("users.id")),
#     Column("permission_id", Integer, ForeignKey("permissions.id"))
# )

# class Permission(Base):
#     __tablename__ = 'permissions'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), nullable=False)
#     description = Column(Text, nullable=False)
#     code = Column(String(50), nullable=False)
#     module_name = Column(String(50), nullable=True)

#     created_by_user_id = Column(Integer, ForeignKey("users.id"))
#     creator = relationship("User", back_populates="created_permissions")

#     roles = relationship("Role", secondary="role_permission", back_populates="permissions")
    
#     users = relationship(
#     "User",
#     secondary=user_permission,
#     back_populates="permissions"
# )

    

# # app/models/permission.py
# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base
# from app.models.associations import role_permission, user_permission
# from app.models.mixins import TimeUserStampMixin  # ✅ Added


# class Permission(TimeUserStampMixin, Base):  # ✅ Added TimeUserStampMixin
#     __tablename__ = 'permissions'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), nullable=False)
#     description = Column(Text, nullable=False)
#     code = Column(String(50), nullable=False)
#     module_name = Column(String(50), nullable=True)

#     # ✅ created_by_user_id, updated_by_user_id, deleted_by_user_id now come from mixin
#     # ✅ creator, updater, deleter relationships come from mixin
#     # ✅ created_at, updated_at, deleted, deleted_at come from mixin

#     # Roles with this permission (many-to-many)
#     roles = relationship(
#         "Role", 
#         secondary=role_permission, 
#         back_populates="permissions"
#     )
    
#     # Users with direct permission (many-to-many)
#     users = relationship(
#         "User",
#         secondary=user_permission,
#         back_populates="permissions"
#     )






# app/models/permission.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associations import role_permission, user_permission
from app.models.mixins import TimeUserStampMixin


class Permission(TimeUserStampMixin, Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    module_name = Column(String(50), nullable=True)

    # Relationships
    # Roles with this permission (many-to-many)
    # ✅ KEY FIX: Added lazy="selectin" to eagerly load roles
    roles = relationship(
        "Role",
        secondary=role_permission,
        back_populates="permissions",
        lazy="selectin"  # This ensures roles are loaded automatically
    )
    
    # Users with direct permission (many-to-many)
    users = relationship(
        "User",
        secondary=user_permission,
        back_populates="permissions",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}', code='{self.code}')>"