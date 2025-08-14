from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from models.user import UserCreateSchema, UserLoginSchema, TokenSchema
from services import user_service

router = APIRouter(prefix="/user", tags=["User"])

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["library_db"]
user_collection = db["users"]

@router.post("/signup", response_model=dict)
async def signup(user_data: UserCreateSchema):
    user_id = await user_service.signup_user(user_collection, user_data)
    return {"message": "User created successfully", "id": user_id}

@router.post("/login", response_model=TokenSchema)
async def login(login_data: UserLoginSchema):
    return await user_service.login_user(user_collection, login_data)
