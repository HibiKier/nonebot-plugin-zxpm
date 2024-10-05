from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Bot

from ..log import logger
from ..models.group_console import GroupConsole

nonebot.load_plugins(str(Path(__file__).parent.resolve()))

driver = nonebot.get_driver()


@driver.on_bot_connect
async def _(bot: Bot):
    """将bot已存在的群组添加群认证

    参数:
        bot: Bot
    """
    try:
        group_list = await bot.get_group_list()
        db_group_list = await GroupConsole.all().values_list("group_id", flat=True)
        create_list = []
        for group in group_list:
            gid = str(group["group_id"])
            if gid not in db_group_list:
                logger.debug(f"Bot: {bot.self_id} 添加创建群组Id: {gid}")
                create_list.append(
                    GroupConsole(group_id=gid, group_name=group.get("group_name", ""))
                )
        if create_list:
            await GroupConsole.bulk_create(create_list, 10)
        logger.debug(f"更新Bot: {bot.self_id} 共创建 {len(create_list)} 条群组数据...")
    except Exception as e:
        logger.error(f"获取Bot: {bot.self_id} 群组发生错误...", e=e)
