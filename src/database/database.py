import enum
import typing

import bson
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, TEXT

from src.database import models
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

class SearchTypeForPost(enum.Enum):
    id: bson.ObjectId = "id"
    url: str = "url"

class SearchTypeForRole(enum.Enum):
    id: bson.ObjectId = "id"
    name: str = "name"

class DataBase:
    """
    Class for working with MongoDB
    """
    def __init__(self, db_name: str) -> None:
        """
        Initialize the database connection
        :param db_name: database name
        :return: None
        """
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[db_name]

    async def close_connection(self) -> None:
        """
        Close the database connection.
        :return: None
        """
        self.client.close()


    @async_decorator_info_for_database_log_func
    async def create_index(self, collection_name: str, fields: typing.Union[str, list[tuple]], unique: bool = False, index_type: str = "default") -> None:
        """
        Create an index for a specified collection.

        :param collection_name: Name of the collection
        :param fields: Single field (str) or a list of tuples (field, order)
        :param unique: Whether the index should be unique (default False)
        :param index_type: Type of index ("default" or "text")
        :return: None
        """
        collection = self.db[collection_name]

        if index_type == "text":
            # Text index
            if isinstance(fields, str):
                fields = [(fields, TEXT)]
            else:
                fields = [(field, TEXT) for field, _ in fields]
        elif isinstance(fields, str):
            fields = [(fields, ASCENDING)]

        await collection.create_index(fields, unique=unique)

    @async_decorator_info_for_database_log_func
    async def drop_indexes(self, collection_name: str) -> None:
        """
        Drop all indexes for a specified collection.
        :param collection_name: Name of the collection
        :return: None
        """
        await self.db[collection_name].drop_indexes()


    @async_decorator_info_for_database_log_func
    async def get_all_users(self) -> list[models.UserModel]:
        """
        Get all users
        :return: list of users
        """
        cursor = self.db["users"].find()
        return await cursor.to_list(length=None)

    @async_decorator_info_for_database_log_func
    async def get_user(self, type: SearchTypeForUser, data: str) -> models.UserModel | None:
        """
        Get user
        :param type: search type (SearchTypeForUser)
        :param data: user data
        :return: user
        """
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
    async def create_user(self, user: models.UserModel) -> int:
        """
        Create user
        :param user: user
        :return: user id
        """
        if not isinstance(user, models.UserModel):
            await database_log_func("create_user", "Invalid user data", "critical")
        user_data = user.model_dump(by_alias=True, exclude={"id"})
        result = await self.db["users"].insert_one(user_data)
        return result.inserted_id

    @async_decorator_info_for_database_log_func
    async def set_user_data(self, user_id: bson.ObjectId, data: dict) -> bool:
        """
        Set user data
        :param user_id: user id
        :param data: user data
        :return: True if user data was set
        """
        if not bson.ObjectId.is_valid(user_id):
            await database_log_func("set_user_data", "Invalid user ID", "critical")
            raise ValueError("Invalid user ID")

        filter = {"_id": bson.ObjectId(user_id)}
        update = {"$set": data}

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def add_user_data(self, user_id: bson.ObjectId, data: dict) -> bool:
        """
        Add user data
        :param user_id: user id
        :param data: user data
        :return: True if user data was added
        """
        if not bson.ObjectId.is_valid(user_id):
            await database_log_func("add_user_data", "Invalid user ID", "critical")
            raise ValueError("Invalid user ID")

        filter = {"_id": bson.ObjectId(user_id)}
        update = {"$push": data}

        result = await self.db["users"].update_one(filter, update)
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def search_by_users_attribute(self, attribute: SearchAttributeForUser, data: dict | str) -> list[models.UserModel]:
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


    @async_decorator_info_for_database_log_func
    async def get_role(self, role_id: bson.ObjectId) -> models.PolesModel | None:
        if not bson.ObjectId.is_valid(role_id):
            await database_log_func("get_role", "Invalid role ID", "critical")
            raise ValueError("Invalid role ID")

        role_data = await self.db["roles"].find_one({"_id": bson.ObjectId(role_id)})
        if role_data:
            return models.PolesModel(**role_data)
        return None

    @async_decorator_info_for_database_log_func
    async def get_all_roles(self) -> list:
        cursor = self.db["roles"].find()
        return await cursor.to_list(length=None)

    @async_decorator_info_for_database_log_func
    async def search_by_roles_attribute(self, type: SearchTypeForRole, data: dict | str) -> list:
        if type == SearchTypeForRole.name:
            query = {"name": data}
        elif type == SearchTypeForRole.id:
            query = {"_id": bson.ObjectId(data)}
        else:
            await database_log_func("search_by_roles_attribute", "Invalid search type", "error")
            return None
        cursor = self.db["roles"].find(query)
        return await cursor.to_list(length=None)

    @async_decorator_info_for_database_log_func
    async def create_role(self, role: models.PolesModel) -> bool:
        result = await self.db["roles"].insert_one(role.model_dump(by_alias=True, exclude={"id"}))
        return result.acknowledged

    @async_decorator_info_for_database_log_func
    async def update_role(self, role_id: bson.ObjectId, data: dict) -> bool:
        if not bson.ObjectId.is_valid(role_id):
            await database_log_func("update_role", "Invalid role ID", "critical")
            raise ValueError("Invalid role ID")

        filter = {"_id": bson.ObjectId(role_id)}
        update = {"$set": data}

        result = await self.db["roles"].update_one(filter, update)
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def delete_role(self, role_id: bson.ObjectId) -> bool:
        if not bson.ObjectId.is_valid(role_id):
            await database_log_func("delete_role", "Invalid role ID", "critical")
            raise ValueError("Invalid role ID")

        result = await self.db["roles"].delete_one({"_id": bson.ObjectId(role_id)})
        return result.acknowledged

    @async_decorator_info_for_database_log_func
    async def activate_role(self, role_id: bson.ObjectId) -> bool:
        if not bson.ObjectId.is_valid(role_id):
            await database_log_func("activate_role", "Invalid role ID", "critical")
            raise ValueError("Invalid role ID")

        filter = {"_id": bson.ObjectId(role_id)}
        update = {"$set": {"is_active": True}}

        result = await self.db["roles"].update_one(filter, update)
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def deactivate_role(self, role_id: bson.ObjectId) -> bool:
        if not bson.ObjectId.is_valid(role_id):
            await database_log_func("deactivate_role", "Invalid role ID", "critical")
            raise ValueError("Invalid role ID")

        filter = {"_id": bson.ObjectId(role_id)}
        update = {"$set": {"is_active": False}}

        result = await self.db["roles"].update_one(filter, update)
        return result.modified_count > 0


    @async_decorator_info_for_database_log_func
    async def get_all_posts(self) -> list:
        cursor = self.db["posts"].find()
        return await cursor.to_list(length=None)

    @async_decorator_info_for_database_log_func
    async def get_post(self, type: SearchTypeForPost, data: str) -> models.PostModel | None:
        if type == SearchTypeForPost.url:
            cursor = self.db["posts"].find({"url": data})
        elif type == SearchTypeForPost.id:
            cursor = self.db["posts"].find({"_id": bson.ObjectId(data)})
        else:
            await database_log_func("get_post", "Invalid search type", "error")
            return None
        return await cursor.to_list(length=1)

    @async_decorator_info_for_database_log_func
    async def create_post(self, post: models.PostModel) -> bool:
        result = await self.db["posts"].insert_one(post.model_dump(by_alias=True, exclude={"id"}))
        return result.acknowledged

    @async_decorator_info_for_database_log_func
    async def update_post(self, post_id: bson.ObjectId, data: dict) -> bool:
        if not bson.ObjectId.is_valid(post_id):
            await database_log_func("update_post", "Invalid post ID", "critical")
            raise ValueError("Invalid post ID")

        filter = {"_id": bson.ObjectId(post_id)}
        update = {"$set": data}

        result = await self.db["posts"].update_one(filter, update)
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def delete_post(self, post_id: bson.ObjectId) -> bool:
        if not bson.ObjectId.is_valid(post_id):
            await database_log_func("delete_post", "Invalid post ID", "critical")
            raise ValueError("Invalid post ID")

        result = await self.db["posts"].delete_one({"_id": bson.ObjectId(post_id)})
        return result.deleted_count > 0

    @async_decorator_info_for_database_log_func
    async def activate_post(self, post_id: bson.ObjectId) -> bool:
        if not bson.ObjectId.is_valid(post_id):
            await database_log_func("delete_post", "Invalid post ID", "critical")
            raise ValueError("Invalid post ID")
        result = await self.db["posts"].update_one({"_id": bson.ObjectId(post_id)}, {"$set": {"is_active": True}})
        return result.modified_count > 0

    @async_decorator_info_for_database_log_func
    async def deactivate_post(self, post_id: bson.ObjectId) -> bool:
        if not bson.ObjectId.is_valid(post_id):
            await database_log_func("delete_post", "Invalid post ID", "critical")
            raise ValueError("Invalid post ID")
        result = await self.db["posts"].update_one({"_id": bson.ObjectId(post_id)}, {"$set": {"is_active": False}})
        return result.modified_count > 0