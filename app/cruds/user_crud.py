from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from ..models.user_models import Role, User
from ..schemas.user_schemas import UserCreate, UserUpdateEmail, UserUpdatePassword
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from ..services.utills import get_password_hash


def create_user(db: Session, user: UserCreate):
    # Hash the password before storing it in the database
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password=hashed_password,)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        # Assuming the duplicate email constraint is on the 'email' column
        if "email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        # Handle other IntegrityErrors if necessary, or re-raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        ) from e


def create_super_user(db: Session, email: str, password: str):
    # Hash the password and create a superuser with elevated privileges
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email, 
        password=hashed_password,
        is_superuser=True,
        is_staff=True,
        is_active=True
        )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        # Assuming the duplicate email constraint is on the 'email' column
        if "email" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        # Handle other IntegrityErrors if necessary, or re-raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error"
        ) from e


def read_all_users(db: Session, options: list = None):
    query = db.query(User)
    # Apply eager loading options if provided
    if options:
        query = query.options(*options)
    users = query.all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


def read_user(db: Session, user_id: UUID, options: list = None):
    query = db.query(User).filter(User.u_id == str(user_id))
    # Apply eager loading options if provided
    if options:
        query = query.options(*options)
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def read_user_by_email(db: Session, email: str, options: list = None):
    query = db.query(User).filter(User.email == email)
    # Apply eager loading options if provided
    if options:
        query = query.options(*options)
    user = query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user_email(db: Session, user: UserUpdateEmail):
    db_user = db.query(User).filter(User.u_id == str(user.u_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    email = user.email
    db_user.email = email

    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(db: Session, user: UserUpdatePassword):
    db_user = db.query(User).filter(User.u_id == str(user.u_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    password = get_password_hash(user.password)
    db_user.password = password

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.u_id == str(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return JSONResponse(
        content={"msg": f"User with ID {user_id} has been deleted successfully."},
        status_code=status.HTTP_200_OK,
    )


# ---------------------- Assign role to user crud ----------------------

def assign_role_to_user(db: Session, user_id: str, role_id: int):
    # Get user by UUID with eager loading of roles to optimize role assignment
    user = db.query(User).options(joinedload(User.roles)).filter(User.u_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get role
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Check if user already has the role
    if role in user.roles:
        raise HTTPException(status_code=400, detail="User already has this role")
    
    # Assign role
    user.roles.append(role)
    db.commit()
    return {"message": "Role assigned successfully"}