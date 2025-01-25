import sys
from getpass import getpass
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.database.session import get_db
from app.models.main_models import User
from app.services.utills import get_password_hash

def create_superuser(db: Session, email: str, password: str):
    try:
        user = User(
            email=email,
            passwords=get_password_hash(password),
            is_superuser=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Superuser with email {email} created successfully.")
    except IntegrityError:
        db.rollback()
        print("Error: A user with that email already exists.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")

def main():
    try:
        db = get_db()

        while True:
            try:
                # Prompt for user details
                email = input("Enter email (or type 'q' to exit): ")
                if email.lower() == 'q':
                    print("Operation cancelled by user.")
                    break

                password = getpass("Enter password (or type 'q' to exit): ")
                if password.lower() == 'q':
                    print("Operation cancelled by user.")
                    break

                confirm_password = getpass("Confirm password (or type 'q' to exit): ")
                if confirm_password.lower() == 'q':
                    print("Operation cancelled by user.")
                    break

                if not email or not password:
                    print("Error: All fields are required.")
                    continue

                if password != confirm_password:
                    print("Passwords do not match. Please try again.")
                    continue

                create_superuser(db, email, password)
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
