from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .config import Config
from .enum import PluginType
from .extra import PluginExtraData

require("nonebot_plugin_alconna")
require("nonebot_plugin_session")
require("nonebot_plugin_uninfo")

from .commands import *  # noqa: F403

__plugin_meta__ = PluginMetadata(
    name="ZXPM插件管理",
    description="真寻的插件管理系统",
    usage="""
    包含了插件功能开关，群组/用户ban，群管监测，设置权限功能
    并提供一个简单的帮助接口，可以通过 zxpm [名称] 来获取帮助
    可以通过 -s 参数来获取该功能超级用户帮助
    例如：
        zxpm ban
        zxpm ban -s
    """,
    type="application",
    homepage="https://github.com/HibiKier/nonebot-plugin-zxpm",
    config=Config,
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna",
        "nonebot_plugin_session",
    ),
    extra=PluginExtraData(plugin_type=PluginType.PARENT).to_dict(),
)
