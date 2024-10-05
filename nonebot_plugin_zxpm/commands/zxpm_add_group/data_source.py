from nonebot.adapters import Bot

from ...config import ZxpmConfig
from ...log import logger
from ...models.group_console import GroupConsole
from ...models.level_user import LevelUser
from ...models.plugin_info import PluginInfo


class GroupManager:
    @classmethod
    async def __handle_add_group(
        cls, bot: Bot, group_id: str, group: GroupConsole | None
    ):
        """允许群组并设置群认证，默认群功能开关

        参数:
            bot: Bot
            group_id: 群组id
            group: GroupConsole
        """
        block_plugin = ""
        if plugin_list := await PluginInfo.filter(default_status=False).all():
            for plugin in plugin_list:
                block_plugin += f"<{plugin.module},"
        group_info = await bot.get_group_info(group_id=group_id)
        if group:
            group.block_plugin = block_plugin
            await group.save(update_fields=["block_plugin"])
        else:
            await GroupConsole.create(
                group_id=group_info["group_id"],
                group_name=group_info["group_name"],
                max_member_count=group_info["max_member_count"],
                member_count=group_info["member_count"],
                block_plugin=block_plugin,
            )

    @classmethod
    async def __refresh_level(cls, bot: Bot, group_id: str):
        """刷新权限

        参数:
            bot: Bot
            group_id: 群组id
        """
        admin_default_auth = ZxpmConfig.zxpm_admin_default_auth
        member_list = await bot.get_group_member_list(group_id=group_id)
        member_id_list = [str(user_info["user_id"]) for user_info in member_list]
        flag2u = await LevelUser.filter(
            user_id__in=member_id_list, group_id=group_id
        ).values_list("user_id", flat=True)
        # 即刻刷新权限
        for user_info in member_list:
            user_id = user_info["user_id"]
            role = user_info["role"]
            if user_id in bot.config.superusers:
                await LevelUser.set_level(user_id, user_info["group_id"], 9)
                logger.debug(
                    "添加超级用户权限: 9",
                    "入群检测",
                    session=user_id,
                    group_id=user_info["group_id"],
                )
            elif (
                admin_default_auth is not None
                and role in ["owner", "admin"]
                and user_id not in flag2u
            ):
                await LevelUser.set_level(
                    user_id,
                    user_info["group_id"],
                    admin_default_auth,
                )
                logger.debug(
                    f"添加默认群管理员权限: {admin_default_auth}",
                    "入群检测",
                    session=user_id,
                    group_id=user_info["group_id"],
                )

    @classmethod
    async def add_bot(cls, bot: Bot, group_id: str, group: GroupConsole | None):
        """拉入bot

        参数:
            bot: Bot
            operator_id: 操作者id
            group_id: 群组id
            group: GroupConsole
        """
        await cls.__handle_add_group(bot, group_id, group)
        """刷新群管理员权限"""
        await cls.__refresh_level(bot, group_id)
