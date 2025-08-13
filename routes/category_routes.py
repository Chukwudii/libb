from fastapi import APIRouter, HTTPException
from models.category import CategorySchema
from services import category_service
from models.category import BookItem
from models.category import UpdateCategoryName
from typing import List
router = APIRouter()

@router.post("/", response_model=dict)
async def create_category(category: CategorySchema):
    category_id = await category_service.create_category(category)
    return {"message": "Category created successfully", "id": category_id}

@router.get("/", response_model=list)
async def list_categories():
    return await category_service.get_all_categories()

@router.get("/{category_id}", response_model=dict)
async def get_category(category_id: str):
    category = await category_service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=dict)
async def update_category(category_id: str,  body: UpdateCategoryName):
    updated = await category_service.update_category(category_id, body.category_name)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category updated successfully"}

@router.delete("/{category_id}", response_model=dict)
async def delete_category(category_id: str):
    deleted = await category_service.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

@router.post("/{category_id}/books", response_model=dict)
async def add_book(category_id: str, book: BookItem):
    updated = await category_service.add_books_to_category(
        category_id, [book.model_dump(by_alias=True, exclude_unset=True)]
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Book added successfully"}


@router.put("/{category_id}/books/{book_id}", response_model=dict)
async def update_book(category_id: str, book_id: str, book: BookItem):
    updated = await category_service.update_book_in_category(
        category_id, book_id, book.model_dump(by_alias=True, exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found in category")
    return {"message": "Book updated successfully"}

@router.delete("/{category_id}/books/{book_id}", response_model=dict)
async def delete_book(category_id: str, book_id: str):
    deleted = await category_service.delete_book_from_category(category_id, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found in category")
    return {"message": "Book deleted successfully"}