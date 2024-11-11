from motor.motor_asyncio import AsyncIOMotorClient

from src.app.database import models, blog
from src.config.config import settings


class DataBase:
    def __init__(self, db_name: str) -> None:
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[db_name]

    async def close_connection(self) -> None:
        self.client.close()

    async def get_all_posts(self) -> list:
        cursor = self.db["posts"].find()
        return await cursor.to_list(length=None)

    async def get_post_id(self, post_id: str) -> list:
        cursor = self.db["posts"].find({"_id": post_id})
        return await cursor.to_list(length=1)

    async def create_post(self, post: models.PostModel) -> bool:
        is_new_post = await blog.create_post(post, self.db["posts"])
        if is_new_post:
            return True
        return False