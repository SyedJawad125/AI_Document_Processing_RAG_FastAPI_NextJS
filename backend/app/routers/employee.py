# app/api/routers/employee.py
from fastapi import APIRouter, Depends, Request, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import json
import os

from app import database, schemas, models, oauth2
from app.utils import paginate_data, filter_employees, redis_client
from app.dependencies.permission import require


router = APIRouter(
    prefix="/api/employees",
    tags=['Employees']
)


def invalidate_employee_cache():
    """Invalidate all employee-related cache entries"""
    if redis_client:
        try:
            # Delete all keys matching the pattern
            for key in redis_client.scan_iter("employees_list:*"):
                redis_client.delete(key)
        except Exception as e:
            print(f"Cache invalidation error: {e}")


@router.get("/v1/employee/", response_model=schemas.EmployeeListResponse, dependencies=[require("read_employee")])
def get_employees(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    include_deleted: bool = False,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """Get all employees with pagination and filtering"""
    try:
        # Create cache key
        cache_key = f"employees_list:{str(request.query_params)}:include_deleted:{include_deleted}"

        # Try Redis cache
        if redis_client and not include_deleted:
            cached = redis_client.get(cache_key)
            if cached:
                print("✅ Cache hit")
                cached_data = json.loads(cached)
                serialized_data = [
                    schemas.EmployeeOut(**emp) for emp in cached_data["data"]
                ]
                return {
                    "status": "success",
                    "result": {
                        "count": cached_data["count"],
                        "data": serialized_data
                    }
                }

        # Query based on include_deleted flag
        if include_deleted:
            query = models.Employee.get_all_including_deleted(db)
        else:
            query = models.Employee.get_active(db)

        # Apply filters
        query = filter_employees(request.query_params, query)
        
        total = query.count()
        employees = query.offset(skip).limit(limit).all()

        # Convert to Pydantic
        serialized_data = [schemas.EmployeeOut.from_orm(emp) for emp in employees]

        response_data = {
            "status": "success",
            "result": {
                "count": total,
                "data": serialized_data
            }
        }

        # Cache response
        if redis_client and not include_deleted:
            ttl = int(os.getenv("REDIS_CACHE_TTL", "300"))
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps({
                    "count": total,
                    "data": [emp.model_dump() for emp in serialized_data]
                }, default=str)
            )

        return response_data

    except Exception as e:
        print(f"❌ Error in get_employees: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/v1/employee/{id}", response_model=schemas.EmployeeOut, dependencies=[require("read_employee")])
def get_employee(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Get employee by ID"""
    employee = db.query(models.Employee).filter(
        models.Employee.id == id,
        models.Employee.deleted == False
    ).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {id} not found"
        )
    
    return employee


@router.post("/v1/employee/", 
            status_code=status.HTTP_201_CREATED, 
            response_model=schemas.EmployeeOut, 
            dependencies=[require("create_employee")])
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Create a new employee"""
    try:
        # Check if email already exists (including soft-deleted)
        existing = db.query(models.Employee).filter(
            models.Employee.email == employee.email
        ).first()
        
        if existing and not existing.deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee with this email already exists"
            )
        
        if existing and existing.deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An employee with this email was previously registered. Please use a different email."
            )

        # Create employee with user tracking
        employee_data = employee.model_dump()
        new_employee = models.Employee(
            **employee_data,
            created_by_user_id=current_user.id,
            updated_by_user_id=None
        )
        
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        
        # Invalidate cache
        invalidate_employee_cache()
        
        return new_employee

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating employee: {str(e)}"
        )


@router.patch("/v1/employee/{id}", response_model=schemas.EmployeeOut, dependencies=[require("update_employee")])
def update_employee(
    id: int,
    employee_update: schemas.EmployeeUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Update employee information"""
    try:
        employee = db.query(models.Employee).filter(
            models.Employee.id == id,
            models.Employee.deleted == False
        ).first()

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with id {id} not found"
            )

        # Get update data
        update_data = employee_update.dict(exclude_unset=True)
        
        # Check email uniqueness if email is being updated
        if "email" in update_data and update_data["email"] != employee.email:
            existing = db.query(models.Employee).filter(
                models.Employee.email == update_data["email"],
                models.Employee.id != id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Employee with this email already exists"
                )

        # Update fields
        for key, value in update_data.items():
            setattr(employee, key, value)
        
        # Track who updated
        employee.updated_by_user_id = current_user.id

        db.commit()
        db.refresh(employee)
        
        # Invalidate cache
        invalidate_employee_cache()

        return employee

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating employee: {str(e)}"
        )


@router.delete("/v1/employee/{id}", status_code=status.HTTP_200_OK, dependencies=[require("delete_employee")])
def delete_employee(
    id: int,
    permanent: bool = False,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Soft delete employee (or permanent delete if specified)"""
    employee = db.query(models.Employee).filter(
        models.Employee.id == id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {id} not found"
        )

    if permanent and current_user.is_superuser:
        # Permanent delete (hard delete) - only for superusers
        db.delete(employee)
        db.commit()
        invalidate_employee_cache()
        return {"message": "Employee permanently deleted"}
    else:
        # Soft delete with user tracking
        employee.soft_delete(user_id=current_user.id)
        db.commit()
        invalidate_employee_cache()
        return {"message": "Employee soft deleted successfully"}


@router.post("/v1/employee/{id}/restore", response_model=schemas.EmployeeOut, dependencies=[require("update_employee")])
def restore_employee(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Restore a soft-deleted employee"""
    employee = db.query(models.Employee).filter(
        models.Employee.id == id,
        models.Employee.deleted == True
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deleted employee with id {id} not found"
        )

    employee.restore()
    employee.updated_by_user_id = current_user.id
    db.commit()
    db.refresh(employee)
    
    # Invalidate cache
    invalidate_employee_cache()

    return employee


@router.post("/v1/employee/bulk/upload/", dependencies=[require("create_employee")])
async def upload_employees_bulk(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """Bulk upload employees from Excel/CSV file"""
    try:
        import pandas as pd
        import re
        
        filename = file.filename or ""
        if filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        elif filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xlsx and .csv files are supported"
            )

        df.columns = df.columns.str.strip()

        required_columns = {
            "first_name", "last_name", "email", "phone_number",
            "hire_date", "job_title", "salary"
        }
        
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {missing}"
            )

        existing_emails = {
            e.email for e in db.query(models.Employee.email).filter(
                models.Employee.deleted == False
            ).all()
        }
        
        added_count = 0
        skipped_rows = []
        validation_errors = {}

        for index, row in df.iterrows():
            row_errors = []
            try:
                first_name = str(row["first_name"]).strip()
                last_name = str(row["last_name"]).strip()
                email = str(row["email"]).strip().lower()
                phone_number = str(row["phone_number"]).strip()
                job_title = str(row["job_title"]).strip()

                # Basic validation
                if not first_name or len(first_name) < 1:
                    row_errors.append("Invalid first name")
                if not last_name or len(last_name) < 1:
                    row_errors.append("Invalid last name")
                if email in existing_emails:
                    row_errors.append("Email already exists")
                
                try:
                    hire_date = pd.to_datetime(row["hire_date"], errors='coerce')
                    if pd.isnull(hire_date):
                        row_errors.append("Invalid hire date")
                except:
                    row_errors.append("Invalid hire date format")

                try:
                    salary = float(row["salary"])
                    if salary < 0:
                        row_errors.append("Salary cannot be negative")
                except:
                    row_errors.append("Invalid salary format")

                if row_errors:
                    skipped_rows.append(index + 2)
                    validation_errors[index + 2] = row_errors
                    continue

                # Create employee
                employee = models.Employee(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    hire_date=hire_date.date(),
                    job_title=job_title,
                    salary=salary,
                    created_by_user_id=current_user.id,
                    updated_by_user_id=None
                )
                
                db.add(employee)
                added_count += 1
                existing_emails.add(email)

            except Exception as e:
                skipped_rows.append(index + 2)
                validation_errors[index + 2] = [f"Unexpected error: {str(e)}"]

        db.commit()
        
        # Invalidate cache
        invalidate_employee_cache()

        return {
            "status": "success" if not skipped_rows else "partial_success",
            "message": f"{added_count} employees added. {len(skipped_rows)} rows skipped.",
            "added_count": added_count,
            "skipped_rows": skipped_rows,
            "validation_errors": validation_errors if validation_errors else None
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )