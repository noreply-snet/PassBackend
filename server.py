from typing import Union
from fastapi import FastAPI
from app.database.session import Base,engine

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


predefined_roles = [
    {"name": "Admin", "permissions": ["read_user", "write_user", "delete_user"]},
    {"name": "Editor", "permissions": ["read_user", "write_user"]},
    {"name": "Visitor", "permissions": ["read_user"]},
]

