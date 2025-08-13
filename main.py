from typing import Union
from routes import category_routes
from fastapi import FastAPI
from database import db
app = FastAPI()

app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])

@app.get("/")
async def root():
    collections = await db.list_collection_names()
    return {"message": "Connected!", "collections": collections}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}