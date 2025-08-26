from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
from database import db

VIDEO_COLLECTION = db["videos"]
CATEGORY_COLLECTION = db["categories"]

async def create_video(data: dict) -> str:
    # check category exists
    category = await CATEGORY_COLLECTION.find_one({"_id": ObjectId(data["category_id"])})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    video_doc = {
        "title": data["title"],
        "description": data.get("description"),
        "url": data["url"],
        "category_id": ObjectId(data["category_id"]),
        "created_at": datetime.utcnow()
    }

    result = await VIDEO_COLLECTION.insert_one(video_doc)
    return str(result.inserted_id)


async def get_videos_with_category():
    pipeline = [
        {
            "$lookup": {
                "from": "categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "category_info"
            }
        },
        {"$unwind": "$category_info"},
        {
            "$project": {
                "title": 1,
                "description": 1,
                "url": 1,
                "created_at": 1,
                "category_id": 1,
                "category_name": "$category_info.name"
            }
        }
    ]

    videos = []
    cursor = VIDEO_COLLECTION.aggregate(pipeline)
    async for video in cursor:
        video["_id"] = str(video["_id"])
        video["category_id"] = str(video["category_id"])
        videos.append(video)
    return videos


async def get_video_by_id(video_id: str):
    pipeline = [
        {"$match": {"_id": ObjectId(video_id)}},
        {
            "$lookup": {
                "from": "categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "category_info"
            }
        },
        {"$unwind": "$category_info"},
        {
            "$project": {
                "title": 1,
                "description": 1,
                "url": 1,
                "created_at": 1,
                "category_id": 1,
                "category_name": "$category_info.name"
            }
        }
    ]

    cursor = VIDEO_COLLECTION.aggregate(pipeline)
    video = await cursor.to_list(length=1)

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video = video[0]
    video["_id"] = str(video["_id"])
    video["category_id"] = str(video["category_id"])

    return video



async def update_video(video_id: str, data: dict):
    update_fields = {}
    if "title" in data:
        update_fields["title"] = data["title"]
    if "description" in data:
        update_fields["description"] = data["description"]
    if "url" in data:
        update_fields["url"] = data["url"]
    if "category_id" in data:
        # check if category exists
        category = await CATEGORY_COLLECTION.find_one({"_id": ObjectId(data["category_id"])})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        update_fields["category_id"] = ObjectId(data["category_id"])

    result = await VIDEO_COLLECTION.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": update_fields}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Video not found or no changes applied")
    return True


async def delete_video(video_id: str):
    result = await VIDEO_COLLECTION.delete_one({"_id": ObjectId(video_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Video not found")
    return True
