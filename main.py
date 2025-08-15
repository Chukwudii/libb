from typing import Union
from fastapi import FastAPI
from database import db
from routes import admin_routes
from routes import user_routes
from routes import book_routes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(admin_routes.router)
app.include_router(user_routes.router)
app.include_router(book_routes.router)
@app.get("/")
async def root():
    collections = await db.list_collection_names()
    return {"message": "Connected!", "collections": collections}

