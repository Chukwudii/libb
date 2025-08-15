from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from uuid import uuid4

class BookItem(BaseModel):
    title: str
    author: str
    publisher: str
    category: str
    cover_image: Optional[str] = None  # URL or file path
    downloadable: bool = False


class UpdateBookItem(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    category: Optional[str] = None
    cover_image: Optional[str] = None
    downloadable: Optional[bool] = None