from fastapi import APIRouter, HTTPException
from models.video import VideoCreateSchema, VideoResponseSchema
from services import video_service
from typing import List
router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/", response_model=dict)
async def create_video(video: VideoCreateSchema):
    video_id = await video_service.create_video(video.dict())
    return {"message": "Video created successfully", "id": video_id}

@router.get("/", response_model=List[dict])
async def list_books():
    return await video_service.get_videos_with_category()


@router.get("/{video_id}", response_model=VideoResponseSchema)
async def get_video(video_id: str):
    try:
        return await video_service.get_video_by_id(video_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/category/{category_id}", response_model=list[VideoResponseSchema])
async def get_videos_by_category(category_id: str):
    return await video_service.get_videos_by_category(category_id)


@router.put("/{video_id}", response_model=dict)
async def update_video(video_id: str, video: dict):
    await video_service.update_video(video_id, video)
    return {"message": "Video updated successfully"}


@router.delete("/{video_id}", response_model=dict)
async def delete_video(video_id: str):
    await video_service.delete_video(video_id)
    return {"message": "Video deleted successfully"}
