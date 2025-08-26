from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VideoCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    category_id: str


class VideoResponseSchema(VideoCreateSchema):
    _id: str
    description: Optional[str] = None
    url: str
    category_id: str
    created_at: datetime
    category_name: Optional[str] = None   # ✅ include category name
