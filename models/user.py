from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Signup schema
class UserCreateSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(..., min_length=6)

# Login schema
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

# Response schema
class UserResponseSchema(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# Token schema
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
