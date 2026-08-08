# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
# from sqlalchemy.orm import relationship
# from app.database import Base
# from datetime import datetime
# from app.models.permission import Permission, user_permission

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, index=True, nullable=True)
#     email = Column(String, unique=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, server_default='TRUE', nullable=False)
#     is_superuser = Column(Boolean, server_default='FALSE', nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

#     role_id = Column(Integer, ForeignKey("roles.id"))
#     role = relationship("Role", back_populates="users", foreign_keys=[role_id])
#     created_roles = relationship("Role", back_populates="creator", foreign_keys="Role.created_by_user_id")
#     created_permissions = relationship("Permission", back_populates="creator")
#     permissions = relationship("Permission", secondary=user_permission, back_populates="users")
#     # Employee
#     employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)  # one user per employee
#     employee    = relationship("Employee", back_populates="user")
    


# # app/models/user.py
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base
# from app.models.associations import user_permission
# from app.models.mixins import TimeStampMixin  # ✅ User uses TimeStampMixin only (not UserStampMixin to avoid self-reference)


# class User(TimeStampMixin, Base):  # ✅ Added TimeStampMixin
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, index=True, nullable=True)
#     email = Column(String, unique=True, nullable=False, index=True)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, server_default='TRUE', nullable=False)
#     is_superuser = Column(Boolean, server_default='FALSE', nullable=False)
#     # ✅ created_at, updated_at, deleted, deleted_at now come from TimeStampMixin

#     # Role relationship (one-to-many: User has one role)
#     role_id = Column(Integer, ForeignKey("roles.id"))
#     role = relationship("Role", back_populates="users", foreign_keys=[role_id])
    
#     # Roles created by this user
#     created_roles = relationship(
#         "Role", 
#         back_populates="creator", 
#         foreign_keys="Role.created_by_user_id"
#     )
    
#     # Permissions created by this user
#     created_permissions = relationship("Permission", back_populates="creator")
    
#     # Direct permissions assigned to user (many-to-many)
#     permissions = relationship(
#         "Permission", 
#         secondary=user_permission, 
#         back_populates="users"
#     )
    
#     # Employee relationship (one-to-one)
#     employee_id = Column(Integer, ForeignKey("employees.id"), unique=True)
#     employee = relationship("Employee", back_populates="user")



# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associations import user_permission
from app.models.mixins import TimeStampMixin


class User(TimeStampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    is_superuser = Column(Boolean, server_default='FALSE', nullable=False)

    # Role relationship (one-to-many: User has one role)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users", foreign_keys=[role_id])
    
    # ✅ FIXED: Employee relationship (one-to-one) - specify foreign_keys
    employee = relationship(
        "Employee", 
        back_populates="user", 
        uselist=False,
        foreign_keys="Employee.user_id"  # ✅ Added this
    )
    
    # Roles created/updated/deleted by this user
    created_roles = relationship(
        "Role", 
        back_populates="creator", 
        foreign_keys="Role.created_by_user_id"
    )
    updated_roles = relationship(
        "Role",
        back_populates="updater",
        foreign_keys="Role.updated_by_user_id"
    )
    deleted_roles = relationship(
        "Role",
        back_populates="deleter",
        foreign_keys="Role.deleted_by_user_id"
    )
    
    # Permissions created/updated/deleted by this user
    created_permissions = relationship(
        "Permission", 
        back_populates="creator",
        foreign_keys="Permission.created_by_user_id"
    )
    updated_permissions = relationship(
        "Permission",
        back_populates="updater",
        foreign_keys="Permission.updated_by_user_id"
    )
    deleted_permissions = relationship(
        "Permission",
        back_populates="deleter",
        foreign_keys="Permission.deleted_by_user_id"
    )
    
    # Employees created/updated/deleted by this user
    created_employees = relationship(
        "Employee",
        back_populates="creator",
        foreign_keys="Employee.created_by_user_id"
    )
    updated_employees = relationship(
        "Employee",
        back_populates="updater",
        foreign_keys="Employee.updated_by_user_id"
    )
    deleted_employees = relationship(
        "Employee",
        back_populates="deleter",
        foreign_keys="Employee.deleted_by_user_id"
    )
    
    # ImageCategories created/updated/deleted by this user
    created_imagecategories = relationship(
        "ImageCategory",
        back_populates="creator",
        foreign_keys="ImageCategory.created_by_user_id"
    )
    updated_imagecategories = relationship(
        "ImageCategory",
        back_populates="updater",
        foreign_keys="ImageCategory.updated_by_user_id"
    )
    deleted_imagecategories = relationship(
        "ImageCategory",
        back_populates="deleter",
        foreign_keys="ImageCategory.deleted_by_user_id"
    )
    
    # Images created/updated/deleted by this user
    created_images = relationship(
        "Image",
        back_populates="creator",
        foreign_keys="Image.created_by_user_id"
    )
    updated_images = relationship(
        "Image",
        back_populates="updater",
        foreign_keys="Image.updated_by_user_id"
    )
    deleted_images = relationship(
        "Image",
        back_populates="deleter",
        foreign_keys="Image.deleted_by_user_id"
    )
    
    # Direct permissions assigned to user (many-to-many)
    permissions = relationship(
        "Permission", 
        secondary=user_permission, 
        back_populates="users"
    )