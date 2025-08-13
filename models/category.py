from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class BookItem(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    title: str
    author: str
    publisher: str
    cover_image: Optional[str] = None  # URL or file path
    downloadable: bool = False

class CategorySchema(BaseModel):
    category_name: str
    books: List[BookItem] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UpdateCategoryName(BaseModel):
    category_name: str
