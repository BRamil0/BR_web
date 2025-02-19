import datetime

import pydantic, pydantic_core
import typing
import bson

class PyObjectId(bson.ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source: any, handler) -> pydantic_core.core_schema.CoreSchema:
        return pydantic_core.core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if isinstance(v, bson.ObjectId):
            return v
        if isinstance(v, str) and bson.ObjectId.is_valid(v):
            return bson.ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        schema = handler(schema)
        schema.update(type="string", format="objectid")
        return schema

class ImageModel(pydantic.BaseModel):
    URL: typing.Union[dict[str, str], list[str], str, None] = None
    B64: typing.Union[dict[str, str], list[str], str, None] = None

    model_version: int | str = 1

class PermissionsBaseModel(pydantic.BaseModel):
    class RolesPermissionModel(pydantic.BaseModel):
        create_role: bool = False
        edit_role: bool = False
        delete_role: bool = False

    class PostPermissionModel(pydantic.BaseModel):
        create_post: bool = False
        view_post: bool = True
        edit_post: bool = False
        delete_post: bool = False

    root: bool = False
    site_administration_panel: bool = False

    roles_permission: RolesPermissionModel = RolesPermissionModel()
    blog_permission: PostPermissionModel = PostPermissionModel()

    date_added: datetime.datetime
    end_date: datetime.datetime | None = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        protected_namespaces = ()

class RolesModel(PermissionsBaseModel, pydantic.BaseModel):
    class LanguageNameModel(pydantic.BaseModel):
        name: str
        language_code: str

    class ThemeColorModel(pydantic.BaseModel):
        theme: str
        color: str | None = None

    id: PyObjectId | None = pydantic.Field(default=None, alias="_id")
    default_name: str
    default_color: str | None = None

    language_name: list[LanguageNameModel | None] = pydantic.Field(default_factory=lambda: [])
    theme_color: list[ThemeColorModel | None] = pydantic.Field(default_factory=lambda: [])

    is_active: bool = True

    model_version: int | str = 1


class PermissionsModel(PermissionsBaseModel, pydantic.BaseModel):
    id: PyObjectId | None = pydantic.Field(default=None, alias="_id")
    user_id: PyObjectId | None = None

    model_version: int | str = 1

class UserModel(pydantic.BaseModel):
    class EmailModel(pydantic.BaseModel):
        email: pydantic.EmailStr
        is_verified: bool

    class PhoneNumberModel(pydantic.BaseModel):
        phone_number: str
        is_verified: bool

    class LoginSessionModel(pydantic.BaseModel):
        token: str
        device_name: str | None = None
        user_agent: str | None = None
        is_active: bool = True
        login_time: datetime.datetime
        ip_address: str | None = None

    class RoleModel(pydantic.BaseModel):
        id: PyObjectId
        at_added: datetime.datetime | None = None
        at_works_until: datetime.datetime | None = None

        class Config:
            populate_by_name = True

    class OAuthLinkModel(pydantic.BaseModel):
        pass

    id: typing.Optional[PyObjectId] = pydantic.Field(default=None, alias="_id")

    username: str
    email: list[EmailModel | None] = pydantic.Field(default_factory=lambda: []) # for example [{email: test@test, is_verified: False}, {email: test2@test2, is_verified: True}]
    phone_number: list[PhoneNumberModel | None] = pydantic.Field(default_factory=lambda: []) # for example [{phone_number: +380123456789, is_verified: False}, {phone_number: +380987654321, is_verified: True}]

    login_sessions: list[LoginSessionModel | None] = pydantic.Field(default_factory=lambda: [])
    oauth_links: list[typing.Dict[str, str]] = pydantic.Field(default_factory=lambda: []) # is a list of links to other accounts via OAuth services

    roles: list[RoleModel | None] = pydantic.Field(default_factory=lambda: []) # it's like what the user can do, for example, if the word admin is there, then the user has access to the admin panel

    password: str
    is_password_active: bool = True

    created_at: datetime.datetime
    updated_at: datetime.datetime

    is_active: bool = False

    model_version: int | str = 1

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        protected_namespaces = ()

class SettingsModel(pydantic.BaseModel):
    id: PyObjectId | None = pydantic.Field(default=None, alias="_id")
    user_id : PyObjectId | None = None

    about_me: str | None = None
    language: str | None = None
    theme: str | None = None
    profile_photo_image: list[ImageModel | None] = pydantic.Field(default_factory=lambda: [])
    background_image: list[ImageModel | None] = pydantic.Field(default_factory=lambda: [])

    model_version: int | str = 1

class PostModel(pydantic.BaseModel):
    class ContentModel(pydantic.BaseModel):
        title: str | None = None
        content: str | None = None
        author: str | None = None
        language: str | None = None
        description: str | None = None
        image: ImageModel = pydantic.Field(default_factory=ImageModel)

    id: typing.Optional[PyObjectId] = pydantic.Field(default=None, alias="_id")
    url: str
    user_id: PyObjectId | None = None
    contents: list[ContentModel | None] = pydantic.Field(default_factory=lambda: [])
    created_at: datetime.datetime
    updated_at: datetime.datetime
    default_image: ImageModel = pydantic.Field(default_factory=ImageModel)
    is_active: bool = True

    model_version: int | str = 1

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
        protected_namespaces = ()

