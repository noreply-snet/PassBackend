from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Table,
    func,
)
from sqlalchemy.orm import relationship
import uuid
from ..database.session import Base


# ------------------- User Model ---------------------
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

    # Relationships
    roles = relationship("Role", secondary="user_roles", back_populates="users")

    # Other relationships to specific models
    atms = relationship("AtmDataModel", back_populates="user")
    banks = relationship("BankDataModel", back_populates="user")
    passwords = relationship("PassDataModel", back_populates="user")
    notes = relationship("NoteDataModel", back_populates="user")

    def __repr__(self):
        return (
            f"<User(email='{self.email}', is_superuser={self.is_superuser},"
            f"is_active={self.is_active}, is_staff={self.is_staff})>"
        )


# ------------------- Role Model ---------------------
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Role name (e.g., Admin, User)
    description = Column(String)  # Optional description of the role

    # Relationships
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
    users = relationship("User", secondary="user_roles", back_populates="roles")

    def __repr__(self):
        return f"<Role(name='{self.name}')>"


# ------------------- Permission Model ---------------------
class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Permission name (e.g., view_dashboard)
    description = Column(String)  # Optional description of the permission

    # Relationships
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")

    def __repr__(self):
        return f"<Permission(name='{self.name}')>"


# ------------------- Association Tables ---------------------

# Many-to-Many relationship between Roles and Permissions
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)

# Many-to-Many relationship between Users and Roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.u_id"), primary_key=True),  # Reference `users.u_id`
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),  # Reference `roles.id`
)
