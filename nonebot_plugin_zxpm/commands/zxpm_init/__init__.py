import nonebot
from nonebot import get_loaded_plugins
from nonebot.drivers import Driver
from nonebot.plugin import Plugin, PluginMetadata
from ruamel.yaml import YAML

from ...enum import PluginType
from ...extra import PluginExtraData, PluginSetting
from ...log import logger
from ...models.plugin_info import PluginInfo
from ...models.plugin_limit import PluginLimit
from .manager import manager

_yaml = YAML(pure=True)
_yaml.allow_unicode = True
_yaml.indent = 2

driver: Driver = nonebot.get_driver()


async def _handle_setting(
    plugin: Plugin,
    plugin_list: list[PluginInfo],
    limit_list: list[PluginLimit],
):
    """处理插件设置

    参数:
        plugin: Plugin
        plugin_list: 插件列表
        limit_list: 插件限制列表
    """
    metadata = plugin.metadata
    if not metadata:
        if not plugin.sub_plugins:
            return
        """父插件"""
        metadata = PluginMetadata(name=plugin.name, description="", usage="")
    extra = metadata.extra
    extra_data = PluginExtraData(**extra)
    logger.debug(f"{metadata.name}:{plugin.name} -> {extra}", "初始化插件数据")
    setting = extra_data.setting or PluginSetting()
    if metadata.type == "library":
        extra_data.plugin_type = PluginType.HIDDEN
    if extra_data.plugin_type == PluginType.HIDDEN:
        extra_data.menu_type = ""
    if plugin.sub_plugins:
        extra_data.plugin_type = PluginType.PARENT
    plugin_list.append(
        PluginInfo(
            module=plugin.name,
            module_path=plugin.module_name,
            name=metadata.name,
            author=extra_data.author,
            version=extra_data.version,
            level=setting.level,
            default_status=setting.default_status,
            limit_superuser=setting.limit_superuser,
            menu_type=extra_data.menu_type,
            cost_gold=setting.cost_gold,
            plugin_type=extra_data.plugin_type,
            admin_level=extra_data.admin_level,
            parent=(plugin.parent_plugin.module_name if plugin.parent_plugin else None),
        )
    )
    if extra_data.limits:
        limit_list.extend(
            PluginLimit(
                module=plugin.name,
                module_path=plugin.module_name,
                limit_type=limit._type,
                watch_type=limit.watch_type,
                status=limit.status,
                check_type=limit.check_type,
                result=limit.result,
                cd=getattr(limit, "cd", None),
                max_count=getattr(limit, "max_count", None),
            )
            for limit in extra_data.limits
        )


@driver.on_startup
async def _():
    """
    初始化插件数据配置
    """
    plugin_list: list[PluginInfo] = []
    limit_list: list[PluginLimit] = []
    module2id = {}
    load_plugin = []
    if module_list := await PluginInfo.all().values("id", "module_path"):
        module2id = {m["module_path"]: m["id"] for m in module_list}
    for plugin in get_loaded_plugins():
        load_plugin.append(plugin.module_name)
        await _handle_setting(plugin, plugin_list, limit_list)
    create_list = []
    update_list = []
    for plugin in plugin_list:
        if plugin.module_path not in module2id:
            create_list.append(plugin)
        else:
            plugin.id = module2id[plugin.module_path]
            await plugin.save(
                update_fields=[
                    "name",
                    "author",
                    "version",
                    "admin_level",
                    "plugin_type",
                ]
            )
            update_list.append(plugin)
    if create_list:
        await PluginInfo.bulk_create(create_list, 10)
    await PluginInfo.filter(module_path__in=load_plugin).update(load_status=True)
    await PluginInfo.filter(module_path__not_in=load_plugin).update(load_status=False)
    manager.init()
    if limit_list:
        for limit in limit_list:
            if not manager.exist(limit.module_path, limit.limit_type):
                """不存在，添加"""
                manager.add(limit.module_path, limit)
    manager.save_file()
    await manager.load_to_db()
