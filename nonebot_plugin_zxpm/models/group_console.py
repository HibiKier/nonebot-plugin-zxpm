from tortoise import fields
from typing_extensions import Self

from ..db_connect import Model


class GroupConsole(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    group_id = fields.CharField(255, description="群组id")
    """群聊id"""
    channel_id = fields.CharField(255, null=True, description="频道id")
    """频道id"""
    group_name = fields.TextField(default="", description="群组名称")
    """群聊名称"""
    max_member_count = fields.IntField(default=0, description="最大人数")
    """最大人数"""
    member_count = fields.IntField(default=0, description="当前人数")
    """当前人数"""
    status = fields.BooleanField(default=True, description="群状态")
    """群状态"""
    level = fields.IntField(default=5, description="群权限")
    """群权限"""
    is_super = fields.BooleanField(
        default=False, description="超级用户指定，可以使用全局关闭的功能"
    )
    """超级用户指定群，可以使用全局关闭的功能"""
    block_plugin = fields.TextField(default="", description="禁用插件")
    """禁用插件"""
    superuser_block_plugin = fields.TextField(
        default="", description="超级用户禁用插件"
    )

    class Meta:  # type: ignore
        table = "zxpm_group_console"
        table_description = "群组信息表"
        unique_together = ("group_id", "channel_id")

    @classmethod
    async def get_group(
        cls, group_id: str, channel_id: str | None = None
    ) -> Self | None:
        """获取群组

        参数:
            group_id: 群组id
            channel_id: 频道id.

        返回:
            Self: GroupConsole
        """
        if channel_id:
            return await cls.get_or_none(group_id=group_id, channel_id=channel_id)
        return await cls.get_or_none(group_id=group_id, channel_id__isnull=True)

    @classmethod
    async def is_super_group(cls, group_id: str) -> bool:
        """是否超级用户指定群

        参数:
            group_id: 群组id

        返回:
            bool: 是否超级用户指定群
        """
        return group.is_super if (group := await cls.get_group(group_id)) else False

    @classmethod
    async def is_superuser_block_plugin(cls, group_id: str, module: str) -> bool:
        """查看群组是否超级用户禁用功能

        参数:
            group_id: 群组id
            module: 模块名称

        返回:
            bool: 是否禁用被动
        """
        return await cls.exists(
            group_id=group_id,
            superuser_block_plugin__contains=f"<{module},",
        )

    @classmethod
    async def is_block_plugin(cls, group_id: str, module: str) -> bool:
        """查看群组是否禁用插件

        参数:
            group_id: 群组id
            plugin: 插件名称

        返回:
            bool: 是否禁用插件
        """
        return await cls.exists(
            group_id=group_id, block_plugin__contains=f"<{module},"
        ) or await cls.exists(
            group_id=group_id, superuser_block_plugin__contains=f"<{module},"
        )

    @classmethod
    async def set_block_plugin(
        cls,
        group_id: str,
        module: str,
        is_superuser: bool = False,
    ):
        """禁用群组插件

        参数:
            group_id: 群组id
            task: 任务模块
            is_superuser: 是否为超级用户
        """
        group, _ = await cls.get_or_create(group_id=group_id)
        if is_superuser:
            if f"<{module}," not in group.superuser_block_plugin:
                group.superuser_block_plugin += f"<{module},"
        elif f"<{module}," not in group.block_plugin:
            group.block_plugin += f"<{module},"
        await group.save(update_fields=["block_plugin", "superuser_block_plugin"])

    @classmethod
    async def set_unblock_plugin(
        cls,
        group_id: str,
        module: str,
        is_superuser: bool = False,
    ):
        """禁用群组插件

        参数:
            group_id: 群组id
            task: 任务模块
            is_superuser: 是否为超级用户
        """
        group, _ = await cls.get_or_create(group_id=group_id)
        if is_superuser:
            if f"<{module}," in group.superuser_block_plugin:
                group.superuser_block_plugin = group.superuser_block_plugin.replace(
                    f"<{module},", ""
                )
        elif f"<{module}," in group.block_plugin:
            group.block_plugin = group.block_plugin.replace(f"<{module},", "")
        await group.save(update_fields=["block_plugin", "superuser_block_plugin"])

    @classmethod
    async def is_normal_block_plugin(
        cls, group_id: str, module: str, channel_id: str | None = None
    ) -> bool:
        """查看群组是否禁用功能

        参数:
            group_id: 群组id
            module: 模块名称
            channel_id: 频道id

        返回:
            bool: 是否禁用被动
        """
        return await cls.exists(
            group_id=group_id,
            channel_id=channel_id,
            block_plugin__contains=f"<{module},",
        )

    @classmethod
    async def is_superuser_block_task(cls, group_id: str, task: str) -> bool:
        """查看群组是否超级用户禁用被动

        参数:
            group_id: 群组id
            task: 模块名称

        返回:
            bool: 是否禁用被动
        """
        return await cls.exists(
            group_id=group_id,
            superuser_block_task__contains=f"<{task},",
        )

    @classmethod
    async def is_block_task(
        cls, group_id: str, task: str, channel_id: str | None = None
    ) -> bool:
        """查看群组是否禁用被动

        参数:
            group_id: 群组id
            task: 任务模块
            channel_id: 频道id

        返回:
            bool: 是否禁用被动
        """
        if not channel_id:
            return await cls.exists(
                group_id=group_id,
                channel_id__isnull=True,
                block_task__contains=f"<{task},",
            ) or await cls.exists(
                group_id=group_id,
                channel_id__isnull=True,
                superuser_block_task__contains=f"<{task},",
            )
        return await cls.exists(
            group_id=group_id, channel_id=channel_id, block_task__contains=f"<{task},"
        ) or await cls.exists(
            group_id=group_id,
            channel_id__isnull=True,
            superuser_block_task__contains=f"<{task},",
        )
