import datetime

import pydantic
import typing
import bson


class UserModel(pydantic.BaseModel):
    id: typing.Optional[bson.ObjectId] = pydantic.Field(default=None, alias="_id")
    username: str
    email: typing.List[typing.Dict[str, typing.Union[pydantic.EmailStr, bool]]] = [] # for example [{email: test@test, is_verified: False}, {email: test2@test2, is_verified: True}]
    phone_number: typing.List[typing.Dict[str, typing.Union[str, bool]]] = [] # for example [{phone_number: +380123456789, is_verified: False}, {phone_number: +380987654321, is_verified: True}]
    login_sessions: typing.List[typing.Dict[str, typing.Union[str, bool, datetime.datetime]]] = []
    password: str
    is_password_active: bool = True
    roles: typing.List[typing.Optional[str]] = [] # it's like what the user can do, for example, if the word admin is there, then the user has access to the admin panel
    is_active: bool = False
    oauth_links: typing.List[typing.Dict[str, str]] = [] # is a list of links to other accounts via OAuth services
    created_at: datetime.datetime
    updated_at: datetime.datetime
    about_me: str | None = None
    language: str | None = None
    theme: str | None = None
    avatar: str | None = None
    background_image: str | None = None
    model_version: int | str = 1

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            bson.ObjectId: str
        }

    @pydantic.model_validator(mode="before")
    def convert_id(cls, values):
        if "_id" in values:
            values["id"] = values["_id"]
        return values

class PostModel(pydantic.BaseModel):
    id: typing.Optional[int] = pydantic.Field(default=None, alias="_id")
#    language: dict[str, dict[str, str]] # for example {"en": {"title": "Title in English", "content": "Content in English", description: "Description in English", Author: "Author in English", image: "Image in English"}, "ua": {"title": "Заголовок українською", "content": "Зміст українською", description: "Опис українською", Author: "Автор українською", image: "Зображення українською"}}
    title: str
    content: str
    author: str
    description: str
    image: str
    date_creation: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            bson.ObjectId: str
        }

class CreatePostModel(pydantic.BaseModel):
    title: str
    content: str
    author: str
    image: str | None
    description: str | None