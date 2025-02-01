# schemas/role.py
from pydantic import BaseModel
from typing import Optional,List

# ------------------- Permission Schemas ---------------------

class PermissionTrue(BaseModel):
    name: str

class PermissionBase(PermissionTrue):
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class Permission(PermissionBase):
    id: int
    class Config:
        from_attributes = True

# ------------------- Role Schemas ---------------------

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    permissions: List[PermissionTrue]
    class Config:
        from_attributes = True

