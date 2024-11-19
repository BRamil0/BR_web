import enum
import typing

import bson
from motor.motor_asyncio import AsyncIOMotorClient

from src.database import blog, models
from src.config.config import settings
from src.logger.logger import database_log_func
from src.logger.logger_decorator import async_decorator_info_for_database_log_func


class SearchTypeForUser(enum.Enum):
    email: str = "email"
    username: str = "username"
    id: bson.ObjectId = "id"

class SearchAttributeForUser(enum.Enum):
    id: bson.ObjectId = "id"
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

    @async_decorator_info_for_database_log_func
    async def create_user(self, user: models.UserModel) -> int:
        user_data = user.model_dump(by_alias=True, exclude={"id"})
        result = await self.db["users"].insert_one(user_data)
        return result.inserted_id

    @async_decorator_info_for_database_log_func
    async def get_all_users(self) -> list:
        cursor = self.db["users"].find()
        return await cursor.to_list(length=None)

    @async_decorator_info_for_database_log_func
    async def get_user(self, type: SearchTypeForUser, data: str) -> typing.Optional[models.UserModel]:
        try:
            if type == SearchTypeForUser.email:
                user_data = await self.db["users"].find_one({"email": {"$elemMatch": {"email": data}}})
            elif type == SearchTypeForUser.username:
                user_data = await self.db["users"].find_one({"username": data})
            elif type == SearchTypeForUser.id:
                user_data = await self.db["users"].find_one({"_id": bson.ObjectId(data)})
            else:
                await database_log_func("get_user", "Invalid search type", "error")
                return None
        except (TypeError, ValueError) as e:
            await database_log_func("get_user", str(e), "error")
            return None

        if user_data:
            return  models.UserModel(**user_data)
        return None

    @async_decorator_info_for_database_log_func
    async def set_user_data(self, user_id: bson.ObjectId, data: dict) -> bool:
        if not bson.ObjectId.is_valid(user_id):
            await database_log_func("set_user_data", "Invalid user ID", "critical")
            raise ValueError("Invalid user ID")

        filter = {"_id": bson.ObjectId(user_id)}
        update = {"$set": data}

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def add_user_data(self, user_id: bson.ObjectId, data: dict) -> bool:
        if not bson.ObjectId.is_valid(user_id):
            await database_log_func("add_user_data", "Invalid user ID", "critical")
            raise ValueError("Invalid user ID")

        filter = {"_id": bson.ObjectId(user_id)}
        update = {"$push": data}

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def search_by_users_attribute(self, attribute: SearchAttributeForUser, data: dict | str) -> list:
        if isinstance(data, dict):
            query = {attribute.value: {"$elemMatch": data}}
        else:
            query = {attribute.value: data}

        cursor = self.db["users"].find(query)
        return await cursor.to_list(length=None)

    @async_decorator_info_for_database_log_func
    async def search_for_attribute_uniqueness(self, attribute: SearchAttributeForUser, data: dict | str) -> bool:
        if isinstance(data, dict):
            query = {attribute.value: {"$elemMatch": data}}
        else:
            query = {attribute.value: data}

        cursor = self.db["users"].find(query)
        return bool(await cursor.to_list(length=1))

    @async_decorator_info_for_database_log_func
    async def get_login_sessions(self, user_id: bson.ObjectId) -> list:
        if not bson.ObjectId.is_valid(user_id):
            await database_log_func("get_login_sessions", "Invalid user ID", "critical")
            raise ValueError("Invalid user ID")
        user = await self.db["users"].find_one({"_id": bson.ObjectId(user_id)})
        return user.get("login_sessions", [])

    @async_decorator_info_for_database_log_func
    async def add_login_session(self, user_id: bson.ObjectId, session_data: dict) -> bool:
        if not bson.ObjectId.is_valid(user_id):
            await database_log_func("add_login_session", "Invalid user ID", "critical")
            raise ValueError("Invalid user ID")
        data = {"login_sessions": session_data}
        return await self.add_user_data(user_id, data)

    @async_decorator_info_for_database_log_func
    async def update_login_session_token(self, user_id: bson.ObjectId, token: str, is_active: bool) -> bool:
        if not bson.ObjectId.is_valid(user_id):
            await database_log_func("update_login_session_token", "Invalid user ID", "critical")
            raise ValueError("Invalid user ID")

        filter = {
            "_id": bson.ObjectId(user_id),
            "login_sessions.token": token
        }
        update = {
            "$set": {
                "login_sessions.$.is_active": is_active
            }
        }

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def remove_login_session(self, user_id: bson.ObjectId, token: str) -> bool:
        if not bson.ObjectId.is_valid(user_id):
            await database_log_func("remove_login_session", "Invalid user ID", "critical")
            raise ValueError("Invalid user ID")

        filter = {"_id": bson.ObjectId(user_id)}
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

