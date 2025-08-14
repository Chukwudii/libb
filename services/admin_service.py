from passlib.context import CryptContext
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import HTTPException
from models.admin import AdminCreateSchema, AdminLoginSchema, AdminResponseSchema

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

async def signup_admin(collection: AsyncIOMotorCollection, data: AdminCreateSchema) -> str:
    # Check if email exists
    if await collection.find_one({"email": data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    admin_doc = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "created_at": datetime.utcnow()
    }
    result = await collection.insert_one(admin_doc)
    return str(result.inserted_id)

async def login_admin(collection: AsyncIOMotorCollection, data: AdminLoginSchema) -> AdminResponseSchema:
    admin = await collection.find_one({"email": data.email})
    if not admin or not verify_password(data.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return AdminResponseSchema(
        id=str(admin["_id"]),
        name=admin["name"],
        email=admin["email"],
        created_at=admin["created_at"]
    )
