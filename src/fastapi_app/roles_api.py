import datetime

from fastapi import APIRouter, HTTPException, Depends

from src.database.database import DataBase, SearchTypeForUser
from src.database import db_utils
from src.fastapi_app import auth_utils
from src.fastapi_app import models
from src.database import models as models_db


router = APIRouter(
    prefix="/api/roles",
    tags=["roles_api"],
)

@router.get("/get_role/{role_id}")
async def get_role(role_id: str, db: DataBase = Depends(auth_utils.get_database)):
    role = await db.get_role(role_id)
    if role:
        return role
    raise HTTPException(404)

@router.get("/get_roles_for_user/{user_id}")
async def get_roles_for_user(user_id: str, db: DataBase = Depends(auth_utils.get_database)):
    user = await db.get_user(SearchTypeForUser.id, user_id)
    if user:
        if not user.roles: return []
        role_data = []
        for role in user.roles:
            role_data.append(await db.get_role(role.id))
        return role_data
    raise HTTPException(404)

@router.post("/create_role")
async def create_role(role: models.RoleCreate, db: DataBase = Depends(auth_utils.get_database), token_data: dict = Depends(auth_utils.token_verification)):
    user = await db.get_user(SearchTypeForUser.id, token_data["id"])
    if await db_utils.is_permission_in_user(user.id, permission="root", db=db) or await db_utils.is_permission_in_user(user.id, "create_role", db):
        new_role = models_db.RolesModel(date_added=datetime.datetime.now(), **role.model_dump())
        is_created = await db.create_role(new_role)
        if is_created:
            return {"ok": is_created}
    raise HTTPException(403)