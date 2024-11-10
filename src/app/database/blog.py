from motor.motor_asyncio import AsyncIOMotorClient

from src.app.database import models
from src.config.config import settings


async def get_next_id(db_name: str, collection_name: str) -> int:
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    collection = client[db_name][collection_name]
    last: dict = await collection.find_one(sort=[("_id", -1)])
    if last:
        return last["_id"] + 1
    return 1

async def create_post(post_data: models.CreatePostModel, posts_collection=None) -> bool:
    post_data = models.PostModel(**post_data.dict())
    post_data.id = await get_next_id(db_name="blog", collection_name="posts")
    result = await posts_collection.insert_one(post_data.dict(by_alias=True))
    return result.acknowledged
