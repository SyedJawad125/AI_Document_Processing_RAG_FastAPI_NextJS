# from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
# from sqlalchemy.orm import relationship
# from app.database import Base

# role_permission = Table(
#     'role_permission',
#     Base.metadata,
#     Column('role_id', Integer, ForeignKey('roles.id')),
#     Column('permission_id', Integer, ForeignKey('permissions.id'))
# )

# class Role(Base):
#     __tablename__ = 'roles'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), nullable=False)
#     description = Column(Text, nullable=False)
#     code = Column(String(50), nullable=True)

#     created_by_user_id = Column(Integer, ForeignKey("users.id"))
#     # created_by_user_id = Column(Integer)  # temporarily remove FK

#     creator = relationship("User", back_populates="created_roles", foreign_keys=[created_by_user_id])
#     users = relationship("User", back_populates="role", foreign_keys="[User.role_id]")

#     permissions = relationship("Permission", secondary=role_permission, back_populates="roles")



# # app/models/role.py
# from sqlalchemy import Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base
# from app.models.associations import role_permission
# from app.models.mixins import TimeUserStampMixin  # ✅ Added


# class Role(TimeUserStampMixin, Base):  # ✅ Added TimeUserStampMixin
#     __tablename__ = 'roles'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), nullable=False)
#     description = Column(Text, nullable=False)
#     code = Column(String(50), nullable=True)

#     # ✅ created_by_user_id, updated_by_user_id, deleted_by_user_id now come from mixin
#     # ✅ creator, updater, deleter relationships come from mixin
#     # ✅ created_at, updated_at, deleted, deleted_at come from mixin
    
#     # Users with this role
#     users = relationship(
#         "User", 
#         back_populates="role", 
#         foreign_keys="[User.role_id]"
#     )

#     # Permissions for this role (many-to-many)
#     permissions = relationship(
#         "Permission", 
#         secondary=role_permission, 
#         back_populates="roles"
#     )



# app/models/role.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associations import role_permission
from app.models.mixins import TimeUserStampMixin


class Role(TimeUserStampMixin, Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    code = Column(String(50), nullable=True, unique=True)

    # Relationships
    # Users with this role (one-to-many)
    users = relationship(
        "User",
        back_populates="role",
        foreign_keys="[User.role_id]"
    )

    # Permissions for this role (many-to-many)
    # ✅ KEY FIX: Added lazy="selectin" to eagerly load permissions
    permissions = relationship(
        "Permission",
        secondary=role_permission,
        back_populates="roles",
        lazy="selectin"  # This ensures permissions are loaded automatically
    )

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}', code='{self.code}')>"