# app/api/routers/role.py
# COMPLETE FIXED VERSION

from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session, joinedload

from app import database, schemas, models, oauth2
from app.utils import paginate_data, filter_roles
from app.dependencies.permission import require


router = APIRouter(
    prefix="/api/roles",
    tags=['Roles']
)


@router.get("/v1/role/", 
            response_model=schemas.RoleListWithPermissionsResponse,  # ✅ CHANGED
            dependencies=[require("read_role")])
def get_roles(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    include_deleted: bool = False,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Get all roles with pagination and filtering - includes permissions"""
    try:
        # Query based on include_deleted flag
        # ✅ Permissions are loaded via lazy="selectin" in the model
        if include_deleted:
            query = models.Role.get_all_including_deleted(db)
        else:
            query = models.Role.get_active(db)
        
        # Apply filters
        query = filter_roles(request.query_params, query)
        
        total = query.count()
        roles = query.offset(skip).limit(limit).all()

        # Convert ORM to Pydantic - using RoleWithPermissions
        serialized_data = [schemas.RoleWithPermissions.from_orm(role) for role in roles]

        return {
            "status": "success",
            "result": {
                "count": total,
                "data": serialized_data
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/v1/role/{id}", 
            response_model=schemas.RoleWithPermissions, 
            dependencies=[require("read_role")])
def get_role(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Get role by ID with permissions"""
    role = db.query(models.Role).filter(
        models.Role.id == id,
        models.Role.deleted == False
    ).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {id} not found"
        )
    
    return role


@router.post("/v1/role/", 
            status_code=status.HTTP_201_CREATED, 
            response_model=schemas.RoleWithPermissions, 
            dependencies=[require("create_role")])
def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Create a new role with permissions"""
    try:
        # Extract permission IDs
        permission_ids = role.permission_ids or []
        role_data = role.dict(exclude={"permission_ids"})

        # Create Role instance with user tracking
        new_role = models.Role(
            **role_data,
            created_by_user_id=current_user.id,
            updated_by_user_id=None
        )

        # Fetch and assign permissions (only non-deleted)
        if permission_ids:
            permissions = db.query(models.Permission).filter(
                models.Permission.id.in_(permission_ids),
                models.Permission.deleted == False
            ).all()
            
            if len(permissions) != len(permission_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more permission IDs are invalid or deleted"
                )
            
            new_role.permissions = permissions

        db.add(new_role)
        db.commit()
        db.refresh(new_role)

        return new_role

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating role: {str(e)}"
        )


@router.patch("/v1/role/{id}", 
              response_model=schemas.RoleWithPermissions, 
              dependencies=[require("update_role")])
def update_role(
    id: int,
    role_update: schemas.RoleUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Update role information and permissions"""
    try:
        role = db.query(models.Role).filter(
            models.Role.id == id,
            models.Role.deleted == False
        ).first()

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {id} not found"
            )

        update_data = role_update.dict(exclude_unset=True)

        # Update basic fields
        for key in ['name', 'description', 'code']:
            if key in update_data:
                setattr(role, key, update_data[key])

        # Handle permission_ids
        if 'permission_ids' in update_data and update_data['permission_ids'] is not None:
            permission_ids = update_data['permission_ids']
            
            # Fetch permissions (only non-deleted)
            permissions = db.query(models.Permission).filter(
                models.Permission.id.in_(permission_ids),
                models.Permission.deleted == False
            ).all()
            
            if len(permissions) != len(permission_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="One or more permission IDs are invalid or deleted"
                )
            
            # Update permissions
            role.permissions = permissions

        # Track who updated
        role.updated_by_user_id = current_user.id

        db.commit()
        db.refresh(role)

        return role

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating role: {str(e)}"
        )


@router.delete("/v1/role/{id}", 
               status_code=status.HTTP_200_OK, 
               dependencies=[require("delete_role")])
def delete_role(
    id: int,
    permanent: bool = False,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Soft delete role (or permanent delete if superuser)"""
    role = db.query(models.Role).filter(models.Role.id == id).first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {id} not found"
        )

    # Check if role is assigned to any active users
    active_users_count = db.query(models.User).filter(
        models.User.role_id == id,
        models.User.deleted == False
    ).count()
    
    if active_users_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete role. It is assigned to {active_users_count} active user(s)."
        )

    if permanent and current_user.is_superuser:
        # Permanent delete (hard delete) - only for superusers
        db.delete(role)
        db.commit()
        return {"message": "Role permanently deleted"}
    else:
        # Soft delete with user tracking
        role.soft_delete(user_id=current_user.id)
        db.commit()
        return {"message": "Role soft deleted successfully"}


@router.post("/v1/role/{id}/restore", 
             response_model=schemas.RoleWithPermissions, 
             dependencies=[require("update_role")])
def restore_role(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Restore a soft-deleted role"""
    role = db.query(models.Role).filter(
        models.Role.id == id,
        models.Role.deleted == True
    ).first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deleted role with id {id} not found"
        )

    role.restore()
    role.updated_by_user_id = current_user.id
    db.commit()
    db.refresh(role)

    return role


# ✅ BONUS: Additional endpoints for permission management

@router.post("/v1/role/{role_id}/permissions/{permission_id}", 
            response_model=schemas.RoleWithPermissions,
            dependencies=[require("update_role")])
def add_permission_to_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Add a single permission to a role"""
    role = db.query(models.Role).filter(
        models.Role.id == role_id,
        models.Role.deleted == False
    ).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {role_id} not found"
        )
    
    permission = db.query(models.Permission).filter(
        models.Permission.id == permission_id,
        models.Permission.deleted == False
    ).first()
    
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with id {permission_id} not found"
        )
    
    # Check if permission is already assigned
    if permission not in role.permissions:
        role.permissions.append(permission)
        role.updated_by_user_id = current_user.id
        db.commit()
        db.refresh(role)
    
    return role


@router.delete("/v1/role/{role_id}/permissions/{permission_id}",
              response_model=schemas.RoleWithPermissions,
              dependencies=[require("update_role")])
def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Remove a permission from a role"""
    role = db.query(models.Role).filter(
        models.Role.id == role_id,
        models.Role.deleted == False
    ).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id {role_id} not found"
        )
    
    permission = db.query(models.Permission).filter(
        models.Permission.id == permission_id
    ).first()
    
    if permission and permission in role.permissions:
        role.permissions.remove(permission)
        role.updated_by_user_id = current_user.id
        db.commit()
        db.refresh(role)
    
    return role