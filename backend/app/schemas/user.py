# from pydantic import BaseModel, EmailStr
# from typing import Optional


# class UserBase(BaseModel):
#     email: EmailStr

# # class UserCreate(UserBase):
# #     password: str
# #     role_id: int

# class UserCreate(BaseModel):
#     username: Optional[str] = None
#     email: EmailStr
#     password: str
#     # role_id: int
#     is_superuser: Optional[bool] = False  # default to False
#     role_id: Optional[int] = None         # Optional, validated in endpoint logic


# # class UserLogin(BaseModel):  # This was missing
# #     email: EmailStr
# #     password: 


# class LoginRequest(BaseModel):
#     email: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class UserUpdate(BaseModel):
#     email: Optional[EmailStr] = None
#     password: Optional[str] = None
#     is_active: Optional[bool] = None

# class UserOut(UserBase):
#     id: int
#     is_active: bool
    
#     class Config:
#         from_attributes = True  # Replaces orm_mode in Pydantic v2

# class TokenResponse(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str

# class TokenData(BaseModel):
#     user_id: int | None = None
#     token_type: str | None = None


# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.base import TimeStampSchema


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role_id: Optional[int] = None
    is_superuser: Optional[bool] = False
    
    class Config:
        extra = "forbid"


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    role_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    
    class Config:
        extra = "forbid"


class UserOut(UserBase, TimeStampSchema):
    id: int
    is_active: bool
    is_superuser: bool
    role_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class PaginatedUsers(BaseModel):
    count: int
    data: list[UserOut]


class UserListResponse(BaseModel):
    status: str
    result: PaginatedUsers


# Auth schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    token_type: Optional[str] = None


# ✅ NEW: Nested schemas for relationships
class RoleBasic(BaseModel):
    """Basic role info for nested responses"""
    id: int
    name: str
    code: Optional[str] = None
    description: str
    
    class Config:
        from_attributes = True


class EmployeeBasic(BaseModel):
    """Basic employee info for nested responses"""
    id: int
    first_name: str
    last_name: str
    name: str
    email: EmailStr
    job_title: str
    
    class Config:
        from_attributes = True


class PermissionBasic(BaseModel):
    """Basic permission info for nested responses"""
    id: int
    name: str
    code: str
    module_name: Optional[str] = None
    
    class Config:
        from_attributes = True


# ✅ NEW: User with relationships
class UserWithRole(UserOut):
    """User with role details"""
    role: Optional[RoleBasic] = None
    
    class Config:
        from_attributes = True


class UserWithEmployee(UserOut):
    """User with employee details"""
    employee: Optional[EmployeeBasic] = None
    
    class Config:
        from_attributes = True


class UserWithPermissions(UserOut):
    """User with direct permissions"""
    permissions: List[PermissionBasic] = []
    
    class Config:
        from_attributes = True


class UserDetailed(UserOut):
    """User with all relationship details"""
    role: Optional[RoleBasic] = None
    employee: Optional[EmployeeBasic] = None
    permissions: List[PermissionBasic] = []
    
    class Config:
        from_attributes = True