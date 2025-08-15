from bson import ObjectId
from database import db
from models.book import BookItem, UpdateBookItem
BOOK_COLLECTION = db["books"]
# Create book
async def create_book(book: BookItem):
    book_dict = book.dict()
    result = await BOOK_COLLECTION.insert_one(book_dict)
    return str(result.inserted_id)

# Get all books
async def get_books():
    books = []
    cursor = BOOK_COLLECTION.find()
    async for book in cursor:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string for JSON
        books.append(book)
    return books

# Get a single book by ID
async def get_book_by_id(book_id: str):
    book = await BOOK_COLLECTION.find_one({"_id": ObjectId(book_id)})
    if book:
        book["_id"] = str(book["_id"])
    return book

# Update a book
async def update_book(book_id: str, updated_data: UpdateBookItem):
    update_dict = {k: v for k, v in updated_data.dict().items() if v is not None}
    result = await BOOK_COLLECTION.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_dict}
    )
    return result.modified_count > 0

# Delete a book
async def delete_book(book_id: str):
    result = await BOOK_COLLECTION.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count > 0
