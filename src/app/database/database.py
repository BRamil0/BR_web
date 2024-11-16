import enum
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from src.app.database import models, blog
from src.config.config import settings
from bson import ObjectId

class SearchTypeForUser(enum.Enum):
    email: str = "email"
    username: str = "username"
    id: ObjectId = "id"

class SearchAttributeForUser(enum.Enum):
    id: ObjectId = "id"
    username: str = "username"
    is_active: str = "is_active"
    created_at: str = "created_at"
    updated_at: str = "updated_at"
    about_me: str = "about_me"
    language: str = "language"
    theme: str = "theme"
    avatar: str = "avatar"
    background_image = "background_image"

    email: str = "email"
    phone_number: str = "phone_number"
    roles: str = "roles"
    login_sessions: str = "login_sessions"
    oauth_links: str = "oauth_links"

class DataBase:
    def __init__(self, db_name: str) -> None:
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[db_name]

    async def close_connection(self) -> None:
        self.client.close()

    async def create_user(self, user: models.UserModel) -> int:
        user_data = user.model_dump(by_alias=True, exclude={"id"})
        result = await self.db["users"].insert_one(user_data)
        return result.inserted_id

    async def get_all_users(self) -> list:
        cursor = self.db["users"].find()
        return await cursor.to_list(length=None)

    async def get_user(self, type: SearchTypeForUser, data: str) -> Optional[models.UserModel]:
        try:
            if type == SearchTypeForUser.email:
                user_data = await self.db["users"].find_one({"email": {"$elemMatch": {"email": data}}})
            elif type == SearchTypeForUser.username:
                user_data = await self.db["users"].find_one({"username": data})
            elif type == SearchTypeForUser.id:
                user_data = await self.db["users"].find_one({"_id": ObjectId(data)})
            else:
                return None
        except (TypeError, ValueError):
            return None

        if user_data:
            return  models.UserModel(**user_data)
        return None

    async def set_user_data(self, user_id: ObjectId, data: dict) -> bool:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")

        filter = {"_id": ObjectId(user_id)}
        update = {"$set": data}

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    async def add_user_data(self, user_id: ObjectId, data: dict) -> bool:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")

        filter = {"_id": ObjectId(user_id)}
        update = {"$push": data}

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    async def search_by_users_attribute(self, attribute: SearchAttributeForUser, data: dict | str) -> list:
        if isinstance(data, dict):
            query = {attribute.value: {"$elemMatch": data}}
        else:
            query = {attribute.value: data}

        cursor = self.db["users"].find(query)
        return await cursor.to_list(length=None)

    async def search_for_attribute_uniqueness(self, attribute: SearchAttributeForUser, data: dict | str) -> bool:
        if isinstance(data, dict):
            query = {attribute.value: {"$elemMatch": data}}
        else:
            query = {attribute.value: data}

        cursor = self.db["users"].find(query)
        return bool(await cursor.to_list(length=1))

    async def get_login_sessions(self, user_id: ObjectId) -> list:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")
        user = await self.db["users"].find_one({"_id": ObjectId(user_id)})
        return user.get("login_sessions", [])

    async def add_login_session(self, user_id: ObjectId, session_data: dict) -> bool:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")
        data = {"login_sessions": session_data}
        return await self.add_user_data(user_id, data)

    async def update_login_session_token(self, user_id: ObjectId, token: str, is_active: bool) -> bool:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")

        filter = {
            "_id": ObjectId(user_id),
            "login_sessions.token": token
        }
        update = {
            "$set": {
                "login_sessions.$.is_active": is_active
            }
        }

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    async def remove_login_session(self, user_id: ObjectId, token: str) -> bool:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID")

        filter = {"_id": ObjectId(user_id)}
        update = {"$pull": {"login_sessions": {"token": token}}}

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

