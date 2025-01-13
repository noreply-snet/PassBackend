from fastapi import FastAPI
from app.database.session import Base,engine
from app.apis import atm_api, bank_api, pass_api, note_api
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)


app = FastAPI()

# Configure CORS middleware
origins = [
    "http://localhost:4200",  # Add your Angular frontend origin here
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"বার্তা": "আমি বাংলাতে কথা বলতে পারি । "}


# Include routes
app.include_router(atm_api.router, prefix="/atm", tags=["atm"])
app.include_router(bank_api.router, prefix="/bank", tags=["bank"])
app.include_router(pass_api.router, prefix="/pass", tags=["pass"])
app.include_router(note_api.router, prefix="/note", tags=["note"])



predefined_roles = [
    {"name": "Admin", "permissions": ["read_user", "write_user", "delete_user"]},
    {"name": "Editor", "permissions": ["read_user", "write_user"]},
    {"name": "Visitor", "permissions": ["read_user"]},
]










