from motor.motor_asyncio import AsyncIOMotorClient

from src.database import models
from src.fastapi_app.models import CreatePostModel
from src.config.config import settings

async def get_next_id(db_name: str, collection_name: str) -> int:
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    collection = client[db_name][collection_name]
    last: dict = await collection.find_one(sort=[("_id", -1)])
    print(last)
    if last is None:
        return 0
    return last["_id"] + 1


async def create_post(post_data: CreatePostModel, posts_collection=None, user_id=None) -> bool:
    data = {
        "title": post_data.title,
        "content": post_data.content,
        "author": post_data.author,
        "language": post_data.language,
        "description": post_data.description,
        "image": post_data.image
    }
    post_data = models.PostModel(contents=data, user_id=user_id, URL=post_data.URL)
    result = await posts_collection.insert_one(post_data.model_dump(by_alias=True, exclude={"id"}))
    return result.acknowledged
