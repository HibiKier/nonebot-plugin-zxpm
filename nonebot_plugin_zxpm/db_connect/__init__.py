import nonebot
from tortoise import Tortoise
from tortoise.connection import connections
from tortoise.models import Model as Model_

from ..config import ZxpmConfig
from ..exception import DbConnectError
from ..log import logger

driver = nonebot.get_driver()

MODELS: list[str] = []


class Model(Model_):
    """
    自动添加模块

    Args:
        Model_: Model
    """

    def __init_subclass__(cls, **kwargs):
        MODELS.append(cls.__module__)


@driver.on_startup
async def _():
    try:
        await Tortoise.init(
            db_url=ZxpmConfig.zxpm_db_url,
            modules={"models": MODELS},
            timezone="Asia/Shanghai",
        )
        await Tortoise.generate_schemas()
        logger.info("ZXPM数据库加载完成!")
    except Exception as e:
        raise DbConnectError(f"ZXPM数据库连接错误... e:{e}") from e


@driver.on_shutdown
async def disconnect():
    await connections.close_all()
