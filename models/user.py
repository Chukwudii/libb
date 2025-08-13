from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    created_at: datetime = Field(default_factory=datetime.utcnow)
