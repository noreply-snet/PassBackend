
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import security
from ...database.session import get_db
from ...cruds.role_permission_crud import role_permission_cruds as cruds 
from ...schemas.role_permission_schemas import RoleCreate, RoleUpdate, Role, PermissionCreate, PermissionUpdate, Permission
from ..user.user_api import router as user_router



adminRouter = APIRouter(
    prefix="/access",
    tags=["access"],
)

#-------------Role APIs-------------

roleRouter = APIRouter(
    prefix="/role",
    tags=["role"],
)

@roleRouter.post("/", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return cruds.create_role(db, role)

@roleRouter.get("/{role_id}", response_model=Role)
def read_role(role_id: int, db: Session = Depends(get_db)):
    role = cruds.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@roleRouter.get("/all", response_model=List[Role]) 
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cruds.get_all_roles(db, skip=skip, limit=limit)

@roleRouter.put("/{role_id}", response_model=Role)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    updated_role = cruds.update_role(db, role_id, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role

@roleRouter.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    return cruds.delete_role(db, role_id)


adminRouter.include_router(roleRouter)

#-------------Permission APIs-------------

permissionRouter = APIRouter(
    prefix="/permission",
    tags=["permission"],
)

@permissionRouter.post("/", response_model=Permission)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return cruds.create_permission(db, permission)

@permissionRouter.get("/{permission_id}", response_model=Permission)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = cruds.get_permission(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@permissionRouter.get("/all", response_model=list[Permission])
def read_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cruds.get_all_permissions(db, skip=skip, limit=limit)

@permissionRouter.put("/{permission_id}", response_model=Permission)
def update_permission(
    permission_id: int, 
    permission: PermissionUpdate, 
    db: Session = Depends(get_db)
):
    updated_permission = cruds.update_permission(db, permission_id, permission)
    if not updated_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return updated_permission

@permissionRouter.delete("/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    result = cruds.delete_permission(db, permission_id)
    if not result:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "Permission deleted successfully"}

adminRouter.include_router(permissionRouter)

user_router.include_router(adminRouter)