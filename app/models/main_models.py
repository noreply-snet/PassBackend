from ..database.session import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, func
from datetime import datetime, timezone
from uuid import UUID
import uuid



# ATM Database Model
class AtmDataModel(Base):
    __tablename__ = "atm_data"
    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    exp_date = Column(String, nullable=False)
    cvv = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

# Bank Database Model
class BankDataModel(Base):
    __tablename__ = "bank_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)           # Account holder's name
    bank_name = Column(String, nullable=False)      # Bank name
    branch_name = Column(String, nullable=False)    # Branch name
    acc_type = Column(String, nullable=False)       # Account type (e.g., Savings, Current)
    acc_number = Column(String, nullable=False, unique=True)  # Account number
    ifsc_code = Column(String, nullable=False)      # IFSC code
    mirc_code = Column(String, nullable=True)       # MICR code
    note = Column(Text, nullable=True)              # Additional notes
    rmn = Column(String, nullable=False)            # Registered mobile number
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

# Passwords Database Model
class PassDataModel(Base):
    __tablename__ = "passwords_data"
    id = Column(Integer, primary_key=True, index=True)
    acc_name = Column(String, nullable=False)          # Name of the account
    url = Column(String, nullable=True)                # Website URL
    loginid = Column(String, nullable=False)           # ID used for login to the account (ex- email/username)
    password = Column(String, nullable=False)          # Password
    ass_email = Column(String, nullable=True)          # Associated email
    notes = Column(Text, nullable=True)                # Additional notes
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

# Notes Database Model
class NoteDataModel(Base):
    __tablename__ = "notes_data"
    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing ID
    title = Column(String, nullable=False)             # Title of the note
    tags = Column(JSON(String), nullable=False)       # Array of tags
    massage = Column(Text, nullable=False)             # Note message
    color = Column(String, nullable=False)             # Note color (e.g., hex code)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# Notes Database Model
class User(Base): 
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing ID
    # u_id = Column(UUID(as_uuid=True),index=True, default=uuid.uuid4) # Only for Postgres database
    u_id = Column(String, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    password = Column(String) 
    created_at = Column(DateTime, server_default=func.now()) 
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    