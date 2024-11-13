from motor.motor_asyncio import AsyncIOMotorClient

from src.app.database import models, blog
from src.config.config import settings
from bson import ObjectId


class DataBase:
    def __init__(self, db_name: str) -> None:
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[db_name]

    async def close_connection(self) -> None:
        self.client.close()

    async def get_user_by_email(self, email: str) -> models.UserModel:
        user_data = await self.db["users"].find_one({"email": {"$elemMatch": {"email": email}}})
        if user_data:
            return  models.UserModel(**user_data)
        return None

    async def get_all_users(self) -> list:
        cursor = self.db["users"].find()
        return await cursor.to_list(length=None)

    async def create_user(self, user: models.UserModel) -> int:
        user_data = user.dict(by_alias=True, exclude={"id"})
        result = await self.db["users"].insert_one(user_data)
        return result.inserted_id

    async def get_jwt_tokens(self, user_id: ObjectId) -> list:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")

        user = await self.db["users"].find_one({"_id": ObjectId(user_id)})

        if user and "jwt_tokens" in user:
            return user["jwt_tokens"]
        return []

    async def add_jwt_token(self, user_id: ObjectId, token: str, is_active: bool) -> bool:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")

        filter = {"_id": ObjectId(user_id)}
        update = {"$push": {"jwt_tokens": {"jwt_token": token, "is_active": is_active}}}

        result = await self.db["users"].update_one(filter, update)
        return result.acknowledged

    async def update_jwt_token(self, user_id: ObjectId, token: str, is_active: bool) -> bool:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")

        filter = {
            "_id": ObjectId(user_id),
            "jwt_tokens.jwt_token": token
        }
        update = {
            "$set": {
                "jwt_tokens.$.is_active": is_active
            }
        }

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    async def remove_jwt_token(self, user_id: ObjectId, token: str) -> bool:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")

        filter = {"_id": ObjectId(user_id)}
        update = {"$pull": {"jwt_tokens": {"jwt_token": token}}}

        result = await self.db["users"].update_one(filter, update)
        return result.acknowledged

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