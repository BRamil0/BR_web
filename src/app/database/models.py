import datetime

from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PostModel(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
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