from pydantic import BaseModel

from ..enum import PluginType
from .limit import BaseBlock, PluginCdBlock, PluginCountBlock


class PluginSetting(BaseModel):
    """
    插件基本配置
    """

    level: int = 5
    """群权限等级"""
    default_status: bool = True
    """进群默认开关状态"""
    limit_superuser: bool = False
    """是否限制超级用户"""
    cost_gold: int = 0
    """调用插件花费金币"""


class PluginExtraData(BaseModel):
    """
    插件扩展信息
    """

    author: str | None = None
    """作者"""
    version: str | None = None
    """版本"""
    plugin_type: PluginType = PluginType.NORMAL
    """插件类型"""
    menu_type: str = "功能"
    """菜单类型"""
    admin_level: int | None = None
    """管理员插件所需权限等级"""
    setting: PluginSetting | None = None
    """插件基本配置"""
    limits: list[BaseBlock | PluginCdBlock | PluginCountBlock] | None = None
    """插件限制"""
    superuser_help: str | None = None
    """超级用户帮助"""
