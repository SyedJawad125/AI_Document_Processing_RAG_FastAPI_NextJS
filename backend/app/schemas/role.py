# from typing import Optional, List
# from pydantic import BaseModel
# from app.schemas.permission import Permission as PermissionSchema  # ✅ Use Pydantic schema only

# # Shared base schema
# class RoleBase(BaseModel):
#     name: str
#     description: str
#     code: Optional[str] = None

# # ✅ For role creation
# class RoleCreate(RoleBase):
#     permission_ids: Optional[List[int]] = []

#     class Config:
#         extra = "forbid"  # Prevents unexpected fields like "permissions"

# # ✅ For role update
# class RoleUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     code: Optional[str] = None
#     permission_ids: Optional[List[int]] = []

#     class Config:
#         extra = "forbid"

# # ✅ Role response schema
# class Role(RoleBase):
#     id: int
#     permissions: List[PermissionSchema] = []

#     class Config:
#         from_attributes = True  # Pydantic v2 equivalent of orm_mode

# # ✅ Paginated role list
# class PaginatedRoles(BaseModel):
#     count: int
#     data: List[Role]

# # ✅ Full API response wrapper
# class RoleListResponse(BaseModel):
#     status: str
#     result: PaginatedRoles



# # app/schemas/role.py
# from pydantic import BaseModel, Field
# from typing import Optional
# from app.schemas.base import TimeUserStampSchema  # ✅ Import


# class RoleBase(BaseModel):
#     name: str = Field(..., min_length=1, max_length=50)
#     description: str = Field(..., min_length=1)
#     code: Optional[str] = Field(None, max_length=50)


# class RoleCreate(RoleBase):
#     permission_ids: Optional[list[int]] = []
    
#     class Config:
#         extra = "forbid"


# class RoleUpdate(BaseModel):
#     name: Optional[str] = Field(None, min_length=1, max_length=50)
#     description: Optional[str] = Field(None, min_length=1)
#     code: Optional[str] = Field(None, max_length=50)
#     permission_ids: Optional[list[int]] = None
    
#     class Config:
#         extra = "forbid"


# class RoleOut(RoleBase, TimeUserStampSchema):  # ✅ Now includes all mixin fields
#     id: int
    
#     class Config:
#         from_attributes = True


# class RoleWithPermissions(RoleOut):
#     """Role with permissions details"""
#     from app.schemas.permission import PermissionOut
#     permissions: list[PermissionOut] = []


# class PaginatedRoles(BaseModel):
#     count: int
#     data: list[RoleWithPermissions]


# class RoleListResponse(BaseModel):
#     status: str
#     result: PaginatedRoles



# app/schemas/role.py
from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.base import TimeUserStampSchema


# ✅ Forward declare to avoid circular import
class PermissionOut(BaseModel):
    id: int
    name: str
    description: str
    code: str
    module_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1)
    code: Optional[str] = Field(None, max_length=50)


class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []
    
    class Config:
        extra = "forbid"


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1)
    code: Optional[str] = Field(None, max_length=50)
    permission_ids: Optional[List[int]] = None
    
    class Config:
        extra = "forbid"


class RoleOut(RoleBase, TimeUserStampSchema):
    id: int
    
    class Config:
        from_attributes = True


class RoleWithPermissions(RoleOut):
    """Role with permissions details"""
    permissions: List[PermissionOut] = []
    
    class Config:
        from_attributes = True


# ✅ NEW: Role with user count
class RoleWithStats(RoleOut):
    """Role with statistics"""
    user_count: int = 0
    permission_count: int = 0
    
    class Config:
        from_attributes = True


class PaginatedRoles(BaseModel):
    count: int
    data: List[RoleOut]


class PaginatedRolesWithPermissions(BaseModel):
    count: int
    data: List[RoleWithPermissions]


class RoleListResponse(BaseModel):
    status: str
    result: PaginatedRoles


class RoleListWithPermissionsResponse(BaseModel):
    status: str
    result: PaginatedRolesWithPermissions