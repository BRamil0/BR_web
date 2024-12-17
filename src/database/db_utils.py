import bson

from src.database.database import DataBase, SearchTypeForUser
from src.logger.logger import logger

async def is_permission_in_user(user_id: bson.ObjectId, permission: str, db: DataBase) -> bool:
    user = await db.get_user(SearchTypeForUser.id, user_id)
    try:
        if not user.roles:
            for user_role in user.roles:
                role = await db.get_role(user_role.role_id)
                if await check_permission(role, permission):
                    return True
    except Exception as e:
        logger.opt(colors=True).error(f"<le><b>DataBase</b></le> | <lr>Check permission error <v>{e}</v></lr>")
    return False

async def check_permission(obj, permission):
    for field in obj.__dict__:
        if field not in ['date_added', 'end_date']:
            if getattr(obj, field) == permission:
                return True
            elif hasattr(getattr(obj, field), '__dict__'):
                if await check_permission(getattr(obj, field), permission):
                    return True
    return False