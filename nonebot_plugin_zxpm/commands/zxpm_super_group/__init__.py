from nonebot import logger
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Match,
    Option,
    Subcommand,
    on_alconna,
    store_true,
)
from nonebot_plugin_session import EventSession

from ...enum import PluginType
from ...extra import PluginExtraData
from ...models.group_console import GroupConsole
from ...utils.utils import MessageUtils

__plugin_meta__ = PluginMetadata(
    name="群白名单",
    description="群白名单",
    usage="""
    群白名单
    添加/删除群白名单，当在群组中这五个命令且没有指定群号时，默认指定当前群组
    指令:
        格式:
        group-manage super-handle [群组Id] [--del 删除操作] : 添加/删除群白名单

        快捷:
        group-manage super-handle : 添加/删除群白名单

        示例:
        添加/删除群白名单 1234567                  : 添加/删除 1234567 为群白名单
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.SUPERUSER,
    ).dict(),
)


_matcher = on_alconna(
    Alconna(
        "group-manage",
        Option("--delete", action=store_true, help_text="删除"),
        Subcommand(
            "super-handle",
            Args["group_id?", str],
            help_text="添加/删除群白名单",
        ),
    ),
    permission=SUPERUSER,
    priority=1,
    block=True,
)


_matcher.shortcut(
    "添加群白名单(?P<gid>.*?)",
    command="group-manage",
    arguments=["super-handle", "{gid}"],
    prefix=True,
)

_matcher.shortcut(
    "删除群白名单(?P<gid>.*?)",
    command="group-manage",
    arguments=["super-handle", "{gid}", "--delete"],
    prefix=True,
)


@_matcher.assign("super-handle")
async def _(session: EventSession, arparma: Arparma, group_id: Match[str]):
    if group_id.available:
        gid = group_id.result
    else:
        gid = session.id3 or session.id2
    if not gid:
        await MessageUtils.build_message("群组id不能为空!").finish(reply_to=True)
    group, _ = await GroupConsole.get_or_create(group_id=gid)
    s = "删除" if arparma.find("delete") else "添加"
    group.is_super = not arparma.find("delete")
    await group.save(update_fields=["is_super"])
    await MessageUtils.build_message(f"{s}群白名单成功!").send(reply_to=True)
    logger.info(f"{s}群白名单: {gid}")
