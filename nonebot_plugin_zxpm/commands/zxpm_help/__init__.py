from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import (
    Alconna,
    AlconnaQuery,
    Args,
    Match,
    Option,
    Query,
    on_alconna,
    store_true,
)
from nonebot_plugin_session import EventSession

from ...enum import PluginType
from ...extra import PluginExtraData
from ...log import logger
from ...utils.utils import MessageUtils
from ._data_source import get_plugin_help

__plugin_meta__ = PluginMetadata(
    name="ZXPM帮助",
    description="ZXPM帮助，通过 ZXPM [名称]来获取帮助指令",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.DEPENDANT,
    ).dict(),
)


_matcher = on_alconna(
    Alconna(
        "zxpm",
        Args["name", str],
        Option("-s|--superuser", action=store_true, help_text="超级用户帮助"),
    ),
    aliases={"ZXPM"},
    priority=1,
    block=True,
)


@_matcher.handle()
async def _(
    bot: Bot,
    name: str,
    session: EventSession,
    is_superuser: Query[bool] = AlconnaQuery("superuser.value", False),
):
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    _is_superuser = is_superuser.result if is_superuser.available else False
    if _is_superuser and session.id1 not in bot.config.superusers:
        _is_superuser = False
    if result := await get_plugin_help(session.id1, name, _is_superuser):
        await MessageUtils.build_message(result).send(reply_to=True)
    else:
        await MessageUtils.build_message("没有此功能的帮助信息...").send(reply_to=True)
    logger.info(f"查看帮助详情: {name}", "帮助", session=session)
