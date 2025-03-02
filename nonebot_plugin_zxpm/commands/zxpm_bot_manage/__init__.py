import nonebot
from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from zhenxun_utils.common_utils import CommonUtils
from zhenxun_utils.enum import PluginType
from zhenxun_utils.platform import PlatformUtils

from ...models.bot_console import BotConsole
from ...models.plugin_info import PluginInfo
from .bot_switch import *  # noqa: F403
from .plugin import *  # noqa: F403

driver = nonebot.get_driver()

__plugin_meta__ = PluginMetadata(
    name="Bot管理",
    description="指定bot对象的功能/被动开关和状态",
    usage="""
    指令:
        bot被动状态                 : bot的被动技能状态
        bot开启/关闭被动[被动名称]    : 被动技能开关
        bot开启/关闭所有被动          : 所有被动技能开关
        bot插件列表: bot插件列表状态  : bot插件列表
        bot开启/关闭所有插件          : 所有插件开关
        bot开启/关闭插件[插件名称]    : 插件开关
        bot休眠                    : bot休眠，屏蔽所有消息
        bot醒来                    : bot醒来
    """.strip(),
)

from zhenxun_utils.log import logger


@driver.on_bot_connect
async def init_bot_console(bot: Bot):
    """初始化Bot管理

    参数:
        bot: Bot
    """

    async def _filter_blocked_items(
        items_list: list[str], block_list: list[str]
    ) -> list[str]:
        """过滤被block的项目

        参数:
            items_list: 需要过滤的项目列表
            block_list: block列表

        返回:
            list: 过滤后且经过格式化的项目列表
        """
        return [item for item in items_list if item not in block_list]

    plugin_list = [
        plugin.module
        for plugin in await PluginInfo.get_plugins(
            plugin_type__in=[PluginType.NORMAL, PluginType.DEPENDANT, PluginType.ADMIN]
        )
    ]
    platform = PlatformUtils.get_platform(bot)
    bot_data, created = await BotConsole.get_or_create(
        bot_id=bot.self_id, platform=platform
    )

    if not created:
        plugin_list = await _filter_blocked_items(
            plugin_list, await bot_data.get_plugins(bot.self_id, False)
        )

    bot_data.available_plugins = CommonUtils.convert_module_format(plugin_list)
    await bot_data.save(update_fields=["available_plugins"])
    logger.info("初始化Bot管理完成...")
