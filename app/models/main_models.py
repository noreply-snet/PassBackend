from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, JSON, func, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import uuid
from ..database.session import Base

# ATM Database Model
class AtmDataModel(Base):
    __tablename__ = "atm_data"
    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    exp_date = Column(String, nullable=False)
    cvv = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_u_id = Column(String, ForeignKey('users.u_id'))
    user = relationship("User", back_populates="atms")

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
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_u_id = Column(String, ForeignKey('users.u_id'))
    user = relationship("User", back_populates="banks")

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
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_u_id = Column(String, ForeignKey('users.u_id'))
    user = relationship("User", back_populates="passwords")

# Notes Database Model
class NoteDataModel(Base):
    __tablename__ = "notes_data"
    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing ID
    title = Column(String, nullable=False)             # Title of the note
    tags = Column(JSON(String), nullable=False)       # Array of tags
    message = Column(Text, nullable=False)             # Note message
    color = Column(String, nullable=False)             # Note color (e.g., hex code)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_u_id = Column(String, ForeignKey('users.u_id'))
    user = relationship("User", back_populates="notes")

# User Database Model
class User(Base): 
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing ID
    u_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)  # Indicates if the user is active
    is_superuser = Column(Boolean, default=False)  # Indicates if the user has superuser privileges
    is_staff = Column(Boolean, default=False)  # Indicates if the user is a staff member
    created_at = Column(DateTime, server_default=func.now()) 
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships to other models
    atms = relationship("AtmDataModel", back_populates="user")
    banks = relationship("BankDataModel", back_populates="user")
    passwords = relationship("PassDataModel", back_populates="user")
    notes = relationship("NoteDataModel", back_populates="user")

    def __repr__(self):
        return (f"<User(email='{self.email}', is_superuser={self.is_superuser}, "
                f"is_active={self.is_active}, is_staff={self.is_staff})>")