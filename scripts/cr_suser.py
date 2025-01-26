import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from getpass import getpass
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.cruds.user_crud import create_super_user
from app.database.session import get_db

def main():
    try:
        db = next(get_db())

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

                create_super_user(db, email, password)
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
