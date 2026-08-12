# # permissions_script.py
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
# from app.models.permission import Permission


# # Define all permissions
# PERMISSIONS = [
#     # ---------- Role ----------
#     {"name": "Show Role", "code": "show_role", "module_name": "Role", "description": "User can see role"},
#     {"name": "Create Role", "code": "create_role", "module_name": "Role", "description": "User can create role"},
#     {"name": "Read Role", "code": "read_role", "module_name": "Role", "description": "User can read role"},
#     {"name": "Update Role", "code": "update_role", "module_name": "Role", "description": "User can update role"},
#     {"name": "Delete Role", "code": "delete_role", "module_name": "Role", "description": "User can delete role"},

#     # ---------- User ----------
#     {"name": "Show User", "code": "show_user", "module_name": "User", "description": "User can see user"},
#     {"name": "Create User", "code": "create_user", "module_name": "User", "description": "User can create user"},
#     {"name": "Read User", "code": "read_user", "module_name": "User", "description": "User can read user"},
#     {"name": "Update User", "code": "update_user", "module_name": "User", "description": "User can update user"},
#     {"name": "Delete User", "code": "delete_user", "module_name": "User", "description": "User can delete user"},
#     {"name": "Deactivate User", "code": "toggle_user", "module_name": "User", "description": "User can deactivate user"},

#     # ---------- Image ----------
#     {"name": "Create Image", "code": "create_image", "module_name": "Image", "description": "User can create Image"},
#     {"name": "Read Image", "code": "read_image", "module_name": "Image", "description": "User can read Image"},
#     {"name": "Update Image", "code": "update_image", "module_name": "Image", "description": "User can update Image"},
#     {"name": "Delete Image", "code": "delete_image", "module_name": "Image", "description": "User can delete Image"},

#     # ---------- Image Category ----------
#     {"name": "Create Image Category", "code": "create_image_category", "module_name": "Image Category", "description": "User can create Image Category"},
#     {"name": "Read Image Category", "code": "read_image_category", "module_name": "Image Category", "description": "User can read Image Category"},
#     {"name": "Update Image Category", "code": "update_image_category", "module_name": "Image Category", "description": "User can update Image Category"},
#     {"name": "Delete Image Category", "code": "delete_image_category", "module_name": "Image Category", "description": "User can delete Image Category"},
    
#     # ---------- Permission ----------
#     {"name": "Show Permission", "code": "show_permission", "module_name": "Permission", "description": "User can see Permission"},
#     {"name": "Create Permission", "code": "create_permission", "module_name": "Permission", "description": "User can create Permission"},
#     {"name": "Read Permission", "code": "read_permission", "module_name": "Permission", "description": "User can read Permission"},
#     {"name": "Update Permission", "code": "update_permission", "module_name": "Permission", "description": "User can update Permission"},
#     {"name": "Delete Permission", "code": "delete_permission", "module_name": "Permission", "description": "User can delete Permission"},

#     # ---------- Employee ----------
#     {"name": "Create Employee", "code": "create_employee", "module_name": "Employee", "description": "User can create employee"},
#     {"name": "Read Employee", "code": "read_employee", "module_name": "Employee", "description": "User can read employee"},
#     {"name": "Update Employee", "code": "update_employee", "module_name": "Employee", "description": "User can update employee"},
#     {"name": "Delete Employee", "code": "delete_employee", "module_name": "Employee", "description": "User can delete employee"},
# ]


# def add_permissions_to_db(db: Session):
#     """Add permissions to database if they don't exist"""
#     added_count = 0
#     skipped_count = 0
    
#     for perm_data in PERMISSIONS:
#         existing = db.query(Permission).filter_by(code=perm_data["code"]).first()
#         if not existing:
#             new_perm = Permission(**perm_data)
#             db.add(new_perm)
#             added_count += 1
#             print(f"✅ Added: {perm_data['name']}")
#         else:
#             skipped_count += 1
#             print(f"⏩ Skipped (already exists): {perm_data['name']}")
    
#     db.commit()
    
#     print(f"\n📊 Summary: {added_count} added, {skipped_count} skipped")
#     return db.query(Permission).all()


# def get_all_permissions(db: Session):
#     """Get all permissions from database"""
#     return db.query(Permission).all()


# if __name__ == "__main__":
#     print("🚀 Populating permissions...\n")
#     db = SessionLocal()
#     try:
#         add_permissions_to_db(db)
#         print("\n✅ Permissions populated successfully!")
#     except Exception as e:
#         print(f"\n❌ Error: {str(e)}")
#         db.rollback()
#     finally:
#         db.close()











"""
add_permissions.py
───────────────────
Seeds all Permission records into the database.
Run ONCE after init_db.py.

Usage:
    python add_permissions.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


PERMISSIONS = [
    # ── Documents ─────────────────────────────────────────────────
    {'name': 'Upload Document',   'code_name': 'can_upload_document',   'module_name': 'documents', 'module_label': 'Documents',    'description': 'Upload PDF documents'},
    {'name': 'View Documents',    'code_name': 'can_view_documents',    'module_name': 'documents', 'module_label': 'Documents',    'description': 'View own documents'},
    {'name': 'Delete Document',   'code_name': 'can_delete_document',   'module_name': 'documents', 'module_label': 'Documents',    'description': 'Delete own documents'},
    {'name': 'View All Documents','code_name': 'can_view_all_documents','module_name': 'documents', 'module_label': 'Documents',    'description': 'View all users documents (admin)'},

    # ── Search / Chat ──────────────────────────────────────────────
    {'name': 'Search Documents',  'code_name': 'can_search',            'module_name': 'search',    'module_label': 'Search & Chat','description': 'Search document content'},
    {'name': 'Chat with Document','code_name': 'can_chat',              'module_name': 'chat',      'module_label': 'Search & Chat','description': 'Ask AI questions about documents'},
    {'name': 'Extract Fields',    'code_name': 'can_extract',           'module_name': 'extraction','module_label': 'Search & Chat','description': 'Extract structured data from documents'},
    {'name': 'Generate Summary',  'code_name': 'can_summarize',         'module_name': 'summary',   'module_label': 'Search & Chat','description': 'Generate AI summaries'},
    {'name': 'Download Report',   'code_name': 'can_download_report',   'module_name': 'reports',   'module_label': 'Search & Chat','description': 'Download PDF reports'},

    # ── Users ─────────────────────────────────────────────────────
    {'name': 'View Users',        'code_name': 'can_view_users',        'module_name': 'users',     'module_label': 'User Management','description': 'View user list'},
    {'name': 'Block Users',       'code_name': 'can_block_users',       'module_name': 'users',     'module_label': 'User Management','description': 'Block or unblock users'},

    # ── Roles ─────────────────────────────────────────────────────
    {'name': 'View Roles',        'code_name': 'can_view_roles',        'module_name': 'roles',     'module_label': 'Role Management','description': 'View roles'},
    {'name': 'Create Role',       'code_name': 'can_create_role',       'module_name': 'roles',     'module_label': 'Role Management','description': 'Create new roles'},
    {'name': 'Update Role',       'code_name': 'can_update_role',       'module_name': 'roles',     'module_label': 'Role Management','description': 'Update role permissions'},
    {'name': 'Delete Role',       'code_name': 'can_delete_role',       'module_name': 'roles',     'module_label': 'Role Management','description': 'Delete roles'},

    # ── Companies ─────────────────────────────────────────────────
    {'name': 'View Companies',    'code_name': 'can_view_companies',    'module_name': 'companies', 'module_label': 'Company Management','description': 'View companies'},
    {'name': 'Manage Companies',  'code_name': 'can_manage_companies',  'module_name': 'companies', 'module_label': 'Company Management','description': 'Create/update/delete companies'},
]


async def add_permissions():
    from app.db.database import AsyncSessionLocal
    from app.models.user import Permission
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        added = 0
        for perm_data in PERMISSIONS:
            existing = await db.execute(
                select(Permission).where(Permission.code_name == perm_data['code_name'])
            )
            if existing.scalar_one_or_none():
                print(f'  ⏭  Exists: {perm_data["code_name"]}')
                continue

            perm = Permission(**perm_data)
            db.add(perm)
            added += 1
            print(f'  ✅ Added: {perm_data["code_name"]}')

        await db.commit()
        print(f'\n✅ Done — {added} permissions added, {len(PERMISSIONS) - added} already existed.')


if __name__ == '__main__':
    print('🔑 Adding permissions to database...\n')
    asyncio.run(add_permissions())