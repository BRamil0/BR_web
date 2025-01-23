import datetime

import argon2
import getpass

from src.backend.database.database import DataBase, SearchTypeForRole, SearchTypeForUser
from src.backend.database import models, db_utils
from src.logger.logger import logger
from src.config.config import settings

ph = argon2.PasswordHasher()

async def get_password() -> str:
    while True:
        password_1 = getpass.getpass("root password 1:")
        password_2 = getpass.getpass("root password 2:")
        if password_1 == password_2:
            break
        else:
            logger.opt(colors=True).warning("<le><b>DataBase</b></le> | <lm>Passwords don't match</lm>")
    return ph.hash(password_1)

async def init_account_db():
    db = DataBase("account_info")
    password = await get_password()

    new_user = models.UserModel(
        username="root",
        email=[{"email": "root@web.BR", "is_verified": False}],
        password=password,
        is_active=True,
        roles=[],
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc),
    )
    user_id = await db.create_user(new_user)
    user = await db.get_user(SearchTypeForUser.id, user_id)
    role_root = await db.search_by_roles_attribute(SearchTypeForRole.name, "root")
    await db_utils.assign_role_to_user(user.id, role_root[0].id, db)

async def init_roles_db() -> bool:
    db = DataBase("account_info")
    data = models.RolesModel(
        default_name="root",
        root=True,
        date_added=datetime.datetime.now(),
    )
    result = await db.create_role(data)
    if result:
        logger.opt(colors=True).info(f"<le><b>Roles</b></le> | <lc>Created root role</lc>")
    else:
        logger.opt(colors=True).error(f"<le><b>Roles</b></le> | <lc>Failed to create root role</lc>")
    return result

async def init_blog_db():
    db = DataBase("blogs")

async def init_db():
    while True:
        password = getpass.getpass("Please keep a local password: ")
        if password == settings.LOCAL_PASSWORD:
            break
        else:
            logger.opt(colors=True).warning("<le><b>DataBase</b></le> | <lm>Passwords don't match</lm>")
    if input("You definitely want to continue, but the database must be new or cleaned, otherwise errors may occur (Y/N)") == "Y":
        await init_roles_db()
        await init_account_db()
        await init_blog_db()