import datetime
from src.database.database import DataBase
from src.database import models
from src.logger.logger import logger

async def init_account_db():
    db = DataBase("account_info")

async def init_roles_db() -> bool:
    db = DataBase("account_info")
    data = {
        "default_name": "root",
        "root": True,
        "date_added": datetime.datetime.now(),
    }
    result = await db.create_role(models.RolesModel(**data))
    if result:
        logger.opt(colors=True).info(f"<le><b>Roles</b></le> | <lc>Created root role</lc>")
    else:
        logger.opt(colors=True).error(f"<le><b>Roles</b></le> | <lc>Failed to create root role</lc>")
    return result

async def init_blog_db():
    db = DataBase("blogs")

async def init_db():
    await init_roles_db()
    await init_account_db()
    await init_blog_db()