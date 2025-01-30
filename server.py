from contextlib import asynccontextmanager
from threading import Thread
from fastapi import FastAPI
from app.apis.auth import auth_api
from app.core.setup_db import init_db
from app.database.session import Base, engine
from app.apis.user import atm_api, bank_api, pass_api, note_api, user_api
from fastapi.middleware.cors import CORSMiddleware
from app.services.schedule_task import run_scheduler


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):  # Accept the app instance
    print("Application startup")

    # Initialize the database
    init_db()

    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    yield  # Yield control back to FastAPI

    print("Application shutdown")

# Attach lifespan to FastAPI
app = FastAPI(lifespan=lifespan)


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
app.include_router(user_api.router, prefix="/user", tags=["user"])
app.include_router(auth_api.router, prefix="/auth", tags=["auth"])

