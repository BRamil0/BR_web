from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

class PostModel(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    title: str
    content: str
    author: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @field_validator('id')
    def validate_id(cls, value):
        return value

