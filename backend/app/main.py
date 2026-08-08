# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# # Enable SQLAlchemy logging
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# # Import Base and engine from database (use absolute import)
# from app.database import engine, Base

# # Import all models explicitly (make sure these use Base from database.py)
# from app.models.user import User
# from app.models.department import Department
# from app.models.role import Role
# from app.models.permission import Permission
# from app.models.rank import Rank
# from app.models.attendance import Attendance
# from app.models.timesheet import Timesheet
# from app.models.leave import Leave
# from app.models.notification import Notification
# from app.models.employee_salary import EmployeeSalary
# from app.models.salary_structure import SalaryStructure
# from app.models.payslip import Payslip
# from app.models.salary_history import SalaryHistory
# from app.models.image_category import ImageCategory
# from app.models.image import Image

# # Import routers
# from app.routers import (
#     employee, department, auth, user, 
#     role, permission, rank, attendance, 
#     timesheet, leave, notification, employee_salary,
#     salary_structure, payslip, salary_history, 
#     image_category,
#     image
# )

# app = FastAPI(
#     title="HRM System",
#     version="1.0.0",
#     description="An API for managing HRM features",
#     openapi_tags=[
#         {
#             "name": "Departments",
#             "description": "Operations related to leave creation, approval, and management"
#         },
#         {
#             "name": "Employees",
#             "description": "Employee profile management"
#         },
#         {
#             "name": "Users",
#             "description": "User login and registration"
#         },
#         {
#             "name": "Ranks",
#             "description": "Rank profile management"
#         },
#         {
#             "name": "Roles",
#             "description": "Roles profile management"
#         },
#         {
#             "name": "Notifications",
#             "description": "User notifications management"
#         },
#         {
#             "name": "Image Categories",
#             "description": "Image categories management"
#         }
#     ]
# )
# # CORS settings to allow requests from frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Next.js frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# from fastapi.staticfiles import StaticFiles
# import os
# # Mount static files
# app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# @app.get("/api/hello")
# def read_root():
#     return {"message": "Hello from FastAPI!"}
    
# # # Configure CORS
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # Include routers
# app.include_router(auth.router)
# app.include_router(user.router)
# app.include_router(employee.router)
# app.include_router(department.router)
# app.include_router(role.router)
# app.include_router(permission.router)
# app.include_router(rank.router)
# app.include_router(attendance.router)
# app.include_router(timesheet.router)
# app.include_router(leave.router)
# app.include_router(notification.router)
# app.include_router(employee_salary.router)
# app.include_router(salary_structure.router)
# app.include_router(payslip.router)
# app.include_router(salary_history.router)
# app.include_router(image_category.router)
# app.include_router(image.router)




# @app.on_event("startup")
# def startup_event():
#     print("Creating database tables...")
#     print(f"Engine URL: {engine.url}")
#     print(f"Tables in metadata: {Base.metadata.tables.keys()}")
#     Base.metadata.create_all(bind=engine)
#     print("Database tables created.")


# @app.get("/")
# def root():
#     return {"message": "Welcome to HRM API"}

# @app.get("/ping")
# async def health_check():
#     return {"status": "healthy"}

# @app.get("/test")
# def test():
#     return {"status": "working"}




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Enable SQLAlchemy logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Import Base and engine from database (use absolute import)
from app.database import engine, Base

# Import all models explicitly
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.image import Image, ImageCategory

# Import routers
from app.routers import (
    employee, auth, user, 
    role, permission,image_category, image, 
    house_price_model   # Added house_price_model router
)

app = FastAPI(
    title="HRM System with House Price Prediction",
    version="1.0.0",
    description="An API for managing HRM features with machine learning capabilities",
    openapi_tags=[
        
        {
            "name": "Employees",
            "description": "Employee profile management"
        },
        {
            "name": "Users",
            "description": "User login and registration"
        },
        {
            "name": "Roles",
            "description": "Roles profile management"
        },
        {
            "name": "Image Categories",
            "description": "Image categories management"
        },
        {
            "name": "Machine Learning",
            "description": "House price prediction model"
        }
    ]
)

# CORS settings to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
import os
# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/api/hello")
def read_root():
    return {"message": "Hello from FastAPI!"}

# Include all routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(employee.router)
app.include_router(role.router)
app.include_router(permission.router)
app.include_router(image_category.router)
app.include_router(image.router)
app.include_router(house_price_model.router)  # Added ML router

@app.on_event("startup")
def startup_event():
    print("Creating database tables...")
    print(f"Engine URL: {engine.url}")
    print(f"Tables in metadata: {Base.metadata.tables.keys()}")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

    # Load ML model on startup
    try:
        from app.models.house_price_model import train_and_save_model
        print("Initializing ML model...")
        train_and_save_model()
        print("ML model ready")
    except Exception as e:
        print(f"Error loading ML model: {str(e)}")


@app.get("/")
def root():
    return {"message": "Welcome to HRM API with Machine Learning capabilities"}

@app.get("/")
def read_root():
    return {"message": "Customer Churn Prediction API"}

@app.get("/ping")
async def health_check():
    return {"status": "healthy"}

@app.get("/test")
def test():
    return {"status": "working"}