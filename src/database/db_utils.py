import bson
from fastapi import Depends

from src.fastapi_app.auth_utils import get_database
from src.database.database import DataBase
from src.logger.logger import logger

async def is_permission_in_user(user_id: bson.ObjectId, permission: str, db: DataBase = Depends(get_database)) -> bool:
    user = await db.get_user(user_id)
    try:
        if user.roles is not None:
            for user_role in user.roles:
                role = await db.get_role(user_role.role_id)
                if hasattr(role, permission) and getattr(role, permission) is True:
                    return True
        return False
    except Exception as e:
        logger.opt(colors=True).error(f"<le><b>Database</b></le> | <lc>Check permission error <v>{e}</v></lc>")
    return False