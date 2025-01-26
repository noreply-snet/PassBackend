from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core import security
from ...database.session import get_db
from ...cruds import user_crud as crud
# from ...schemas import user_schemas as schemas
from ..user.user_api import router


adminRouter = APIRouter(
    dependencies=[Depends(security.get_current_user)]
)

@adminRouter.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)

router.include_router(adminRouter)
