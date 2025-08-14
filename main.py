from typing import Union
from routes import category_routes
from fastapi import FastAPI
from database import db
from routes import admin_routes
from routes import user_routes
app = FastAPI()

app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])
app.include_router(admin_routes.router)
app.include_router(user_routes.router)
@app.get("/")
async def root():
    collections = await db.list_collection_names()
    return {"message": "Connected!", "collections": collections}

