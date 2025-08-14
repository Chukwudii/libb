from bson import ObjectId
from database import db
from models.category import CategorySchema
from models.category import UpdateCategoryName
from pydantic import BaseModel
CATEGORY_COLLECTION = db["categories"]
import uuid

# Create Category
async def create_category(category: CategorySchema):
    category_dict = category.model_dump(by_alias=True, exclude=["id"])
    result = await CATEGORY_COLLECTION.insert_one(category_dict)
    return str(result.inserted_id)

# Get All Categories
async def get_all_categories():
    categories = []
    async for category in CATEGORY_COLLECTION.find():
        category["_id"] = str(category["_id"])
        categories.append(category)
    return categories

# Get Single Category
async def get_category_by_id(category_id: str):
    category = await CATEGORY_COLLECTION.find_one({"_id": ObjectId(category_id)})
    if category:
        category["_id"] = str(category["_id"])
    return category

# Update Category (add or modify books)
async def update_category(category_id: str, category_name: str):
    result = await CATEGORY_COLLECTION.update_one(
        {"_id": ObjectId(category_id)},
        {"$set":  {"category_name": category_name}}
    )
    return result.modified_count > 0

# Delete Category
async def delete_category(category_id: str):
    result = await CATEGORY_COLLECTION.delete_one({"_id": ObjectId(category_id)})
    return result.deleted_count > 0


async def add_books_to_category(category_id: str, new_books: list):
    for book in new_books:
        # Use UUIDv4 instead of MongoDB ObjectId for book IDs
        book["id"] = str(uuid.uuid4())

    result = await CATEGORY_COLLECTION.update_one(
        {"_id": ObjectId(category_id)},
        {"$push": {"books": {"$each": new_books}}}
    )
    return result.modified_count > 0
# Update a specific book inside a category
# Update a specific book in a category
async def update_book_in_category(category_id: str, book_id: str, updated_book: dict):
    updated_book["id"] = book_id  # Keep the same UUID
    result = await CATEGORY_COLLECTION.update_one(
        {"_id": ObjectId(category_id), "books.id": book_id},
        {"$set": {"books.$": updated_book}}
    )
    return result.modified_count > 0


# Delete a specific book from a category
async def delete_book_from_category(category_id: str, book_id: str):
    result = await CATEGORY_COLLECTION.update_one(
        {"_id": ObjectId(category_id)},
        {"$pull": {"books": {"id": book_id}}}
    )
    return result.modified_count > 0


