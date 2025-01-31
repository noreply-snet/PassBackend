# crud/role.py
from sqlalchemy.orm import Session
from ..models.user_models import Role, Permission
from ..schemas.role_permission_schemas import PermissionCreate, PermissionUpdate, RoleCreate, RoleUpdate


class CRUDRole_Permission:

# ------------------- Role CRUD ---------------------

    def create_role(self, db: Session, role_in: RoleCreate):
        role = Role(**role_in.model_dump())
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    def get_role(self, db: Session, role_id: int):
        return db.query(Role).filter(Role.id == role_id).first()

    def get_all_roles(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Role).offset(skip).limit(limit).all()

    def update_role(self, db: Session, role_id: int, role_in: RoleUpdate):
        role = db.query(Role).filter(Role.id == role_id).first()
        if role:
            for var, value in vars(role_in).items():
                setattr(role, var, value) if value else None
            db.commit()
            db.refresh(role)
        return role

    def delete_role(self, db: Session, role_id: int):
        role = db.query(Role).filter(Role.id == role_id).first()
        if role:
            db.delete(role)
            db.commit()
        return role

# ------------------- Permission CRUD ---------------------

    def create_permission(self, db: Session, permission_in: PermissionCreate):
        permission = Permission(**permission_in.model_dump())
        db.add(permission)
        db.commit()
        db.refresh(permission)
        return permission

    def get_permission(self, db: Session, permission_id: int):
        return db.query(Permission).filter(Permission.id == permission_id).first()

    def get_all_permissions(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Permission).offset(skip).limit(limit).all()

    def update_permission(self, db: Session, permission_id: int, permission_in: PermissionUpdate):
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if permission:
            for var, value in vars(permission_in).items():
                setattr(permission, var, value) if value else None
            db.commit()
            db.refresh(permission)
        return permission

    def delete_permission(self, db: Session, permission_id: int):
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if permission:
            db.delete(permission)
            db.commit()
        return permission
    

role_permission_cruds = CRUDRole_Permission()