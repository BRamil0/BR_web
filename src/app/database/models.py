import datetime

from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional, List, Dict, Union
from bson import ObjectId


class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    username: str
    email: List[Dict[str, Union[EmailStr, bool]]] = [] # for example [{email: test@test, is_verified: False}, {email: test2@test2, is_verified: True}]
    phone_number: List[Dict[str, Union[str, bool]]] = [] # for example [{phone_number: +380123456789, is_verified: False}, {phone_number: +380987654321, is_verified: True}]
    login_sessions: List[Dict[str, Union[str, bool, datetime.datetime]]] = []
    password: str
    is_password_active: bool = True
    roles: List[Optional[str]] = [] # it's like what the user can do, for example, if the word admin is there, then the user has access to the admin panel
    is_active: bool = False
    oauth_links: List[Dict[str, str]] = [] # is a list of links to other accounts via OAuth services
    created_at: datetime.datetime
    updated_at: datetime.datetime
    about_me: str | None = None
    language: str | None = None
    theme: str | None = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    @model_validator(mode="before")
    def convert_id(cls, values):
        if "_id" in values:
            values["id"] = values["_id"]
        return values

class PostModel(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
#    language: dict[str, dict[str, str]] # for example {"en": {"title": "Title in English", "content": "Content in English", description: "Description in English", Author: "Author in English", image: "Image in English"}, "ua": {"title": "Заголовок українською", "content": "Зміст українською", description: "Опис українською", Author: "Автор українською", image: "Зображення українською"}}
    title: str
    content: str
    author: str
    description: str
    image: str
    date_creation: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            ObjectId: str
        }

class CreatePostModel(BaseModel):
    title: str
    content: str
    author: str
    image: str | None
    description: str | None