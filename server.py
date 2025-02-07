from contextlib import asynccontextmanager
from threading import Thread
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.apis.auth import auth_api
from app.core.setup_db import init_db
from app.database.session import Base, engine
from app.apis.user import atm_api, bank_api, pass_api, note_api, user_api
from app.services.schedule_task import run_scheduler
from app.apis.admin import role_permission_api,manage_user_api


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


middleware = [
    Middleware(HTTPSRedirectMiddleware)
]


# Attach lifespan to FastAPI
app = FastAPI(
    lifespan=lifespan
    # middleware for CSRF Protection (BEST FOR PRODUCTION)
    # middleware=middleware
    )


# Configure CORS middleware
origins = [
    "http://localhost:4200",  # Add your Angular frontend origin here
    "https://medhamitro.onrender.com",  # Add server Angular frontend origin here
    "http://127.0.0.1",
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

# Include routes for Admin
# app.include_router(role_permission_api.adminRouter, prefix="/access", tags=["access"])
# app.include_router(manage_user_api.adminRouter, prefix="/manage", tags=["manage"])
