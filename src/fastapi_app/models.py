import typing
import pydantic

class UserCreate(pydantic.BaseModel):
    username: str
    email: pydantic.EmailStr
    password: str

class Token(pydantic.BaseModel):
    access_token: str
    token_type: str

class LoginForm(pydantic.BaseModel):
    email: str
    password: str

class PasswordChangeForm(pydantic.BaseModel):
    old_password: str
    new_password: str

class ResponseModelForGetCurrentUser(pydantic.BaseModel):
    class ModelUserForGetCurrentUser(pydantic.BaseModel):
        id: str | int
        username: str
        email: list[dict[str, typing.Union[pydantic.EmailStr, bool | int]]]
        phone_number: list[dict[str, typing.Union[str, bool | int]]]
        login_sessions: list[dict[str, typing.Union[str, bool | int]]]
        is_password_active: bool = True
        roles: list[typing.Optional[str]]
        is_active: bool = False
        created_at: str
        updated_at: str
        about_me: str | None = None
        language: str | None = None
        theme: str | None = None
        avatar: str | None = None
        background_image: str | None = None

    user: list[ModelUserForGetCurrentUser]
    message: str
    status: str


class ThemeDefaultListModel(pydantic.BaseModel):
    theme_list: list[str]

class ThemeDefaultModel(pydantic.BaseModel):
    theme_default: str

class LanguageDefaultListModel(pydantic.BaseModel):
    language_list: list[str]

class LanguageDefaultModel(pydantic.BaseModel):
    language_default: str

class CreatePostModel(pydantic.BaseModel):
    class ContentModel(pydantic.BaseModel):
        title: str
        content: str | None = None
        author: str | None = None
        language: str
        description: str | None = None

    url: str
    contents: list[ContentModel]

    class Config:
        from_attributes = True