from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from models.admin import AdminCreateSchema, AdminLoginSchema, AdminResponseSchema
from services import admin_service

router = APIRouter(prefix="/admin", tags=["Admin"])

# MongoDB setup
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["library_db"]
admin_collection = db["admins"]

@router.post("/signup", response_model=dict)
async def signup(admin_data: AdminCreateSchema):
    admin_id = await admin_service.signup_admin(admin_collection, admin_data)
    return {"message": "Admin created successfully", "id": admin_id}

@router.post("/login", response_model=AdminResponseSchema)
async def login(login_data: AdminLoginSchema):
    return await admin_service.login_admin(admin_collection, login_data)
