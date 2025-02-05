from app.database.session import get_db
from app.models.user_models import Role, Permission

actions = {"create", "read", "update", "delete"}
items = {"atm", "bank", "note", "password"}

base_crud = {f"{action}_{item}" for action in actions for item in items}
base_read = {f"read_{item}" for item in items}
base_read_all = {f"read_all_{item}" for item in items}

user_management_lite = {"read_user", "update_user_email", "update_user_password"}
user_management_pro = {"manage_users", "delete_user"}
token_management = {"generate_tokens", "revoke_tokens", "cleanup_tokens"}
other_permissions = {"logout"}


locked_user_permissions = ( base_read | base_read_all | user_management_lite | other_permissions )  # user can only update their own info and read all their items
user_permissions = locked_user_permissions | base_crud # user can actions on all their items 
admin_permissions = ( user_permissions | user_management_pro - {"delete_user"} | token_management ) # admin can manage users except delete_user

all_permissions = admin_permissions | {"delete_user"}

def init_db():
    db = next(get_db())

    # Define roles and permissions
    roles_data = {
        "Admin": admin_permissions,
        "User": user_permissions,
        "Locked-User": locked_user_permissions,
        "Super_Admin": admin_permissions | {"delete_user"},  # Super Admin can delete users
    }

    existing_permissions = {p.name: p for p in db.query(Permission).all()}

    # Add missing permissions to the database
    for perm_name in all_permissions:
        if perm_name not in existing_permissions:
            permission = Permission(name=perm_name)
            db.add(permission)
            db.commit()
            existing_permissions[perm_name] = permission

    # Add roles and assign permissions
    for role_name, perm_names in roles_data.items():
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.commit()
        role.permissions = [existing_permissions[perm] for perm in perm_names]
        db.add(role)
        db.commit()

    db.close()


if __name__ == "__main__":
    init_db()
