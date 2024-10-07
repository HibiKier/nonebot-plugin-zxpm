import contextlib

import nonebot
from nonebot.adapters import Bot
from nonebot_plugin_uninfo import get_interface

from ..log import logger
from ..models.group_console import GroupConsole
from ..models.plugin_info import PluginInfo
from .zxpm_ban import *  # noqa: F403
from .zxpm_help import *  # noqa: F403
from .zxpm_hooks import *  # noqa: F403
from .zxpm_init import *  # noqa: F403
from .zxpm_plugin_switch import *  # noqa: F403
from .zxpm_set_admin import *  # noqa: F403

driver = nonebot.get_driver()

with contextlib.suppress(ImportError):
    from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent  # noqa: F401

    from .zxpm_add_group import *  # noqa: F403
    from .zxpm_admin_watch import *  # noqa: F403


@driver.on_bot_connect
async def _(bot: Bot):
    """更新bot群组信息

    参数:
        bot: Bot
    """
    try:
        if interface := get_interface(bot):
            scens = await interface.get_scenes()
            group_list = [(s.id, s.name) for s in scens if s.is_group]
            db_group_list = await GroupConsole.all().values_list("group_id", flat=True)
            block_modules = await PluginInfo.filter(
                load_status=True, default_status=False
            ).values_list("module", flat=True)
            block_modules = [f"<{module}" for module in block_modules]
            create_list = []
            for gid, name in group_list:
                if gid not in db_group_list:
                    group = GroupConsole(group_id=gid, group_name=name)
                    if block_modules:
                        group.block_plugin = ",".join(block_modules) + ","
                    logger.debug(f"Bot: {bot.self_id} 添加创建群组Id: {group.group_id}")
                    create_list.append(group)
            if create_list:
                await GroupConsole.bulk_create(create_list, 10)
                logger.debug(
                    f"更新Bot: {bot.self_id} 共创建 {len(create_list)} 条群组数据..."
                )
    except Exception as e:
        logger.error(f"获取Bot: {bot.self_id} 群组发生错误...", e=e)
