from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from ...core import security
from ...database.session import get_db
from ...cruds import user_crud as crud
from ..user.user_api import router as user_router


adminRouter = APIRouter(
    dependencies=[Depends(security.get_current_user)],
    prefix="/manage",
    tags=["manage"],
)


@adminRouter.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)


# ------------------- Assign Role to User Endpoint ---------------------
@adminRouter.post("/user/{user_id}/role")
def assign_role_to_user(user_id: UUID, role_id: int, db: Session = Depends(get_db)):
    return crud.assign_role_to_user(db=db, user_id=user_id, role_id=role_id)




user_router.include_router(adminRouter)