from nonebot import on_notice
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import GroupIncreaseNoticeEvent
from nonebot.adapters.onebot.v12 import GroupMemberIncreaseEvent
from nonebot.plugin import PluginMetadata

from ...enum import PluginType
from ...extra import PluginExtraData
from ...models.group_console import GroupConsole
from ...rules import notice_rule
from .data_source import GroupManager

__plugin_meta__ = PluginMetadata(
    name="QQ群事件处理",
    description="群事件处理",
    usage="",
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        plugin_type=PluginType.HIDDEN,
    ).dict(),
)

group_increase_handle = on_notice(
    priority=1,
    block=False,
    rule=notice_rule([GroupIncreaseNoticeEvent, GroupMemberIncreaseEvent]),
)
"""群员增加处理"""


@group_increase_handle.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent | GroupMemberIncreaseEvent):
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    if user_id == bot.self_id:
        """新成员为bot本身"""
        group, _ = await GroupConsole.get_or_create(
            group_id=group_id, channel_id__isnull=True
        )
        await GroupManager.add_bot(bot, group_id, group)
