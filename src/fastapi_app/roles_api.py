import datetime

from fastapi import APIRouter, HTTPException, Depends, Response, Request

from src.database.database import DataBase, SearchTypeForUser
from src.fastapi_app import auth_utils
from src.fastapi_app import models


router = APIRouter(
    prefix="/api/roles",
    tags=["roles_api"],
)

@router.post("/create_role")
async def create_role(role: models.RoleModel, db: DataBase = Depends(auth_utils.get_database), token_data: dict = Depends(auth_utils.token_verification)):
    user = await db.get_user(SearchTypeForUser.id, token_data["id"])

    is_created = await db.create_role(role, token_data["id"])
    return {"ok": is_created}