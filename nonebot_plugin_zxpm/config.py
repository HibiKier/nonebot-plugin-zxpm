from pathlib import Path

import nonebot
from pydantic import BaseModel

DEFAULT_DATA_PATH = Path() / "data" / "zxpm"


class Config(BaseModel):
    zxpm_data_path: str | Path = str(DEFAULT_DATA_PATH.absolute())
    """数据存储路径"""
    zxpm_db_url: str | None = None
    """DB_URL"""
    zxpm_notice_info_cd: int = 300
    """群/用户权限检测等各种检测提示信息cd，为0时不提醒"""
    zxpm_ban_reply: str = "才不会给你发消息."
    """用户被ban时回复消息，为空时不回复"""
    zxpm_ban_level: int = 5
    """使用ban功能的对应权限"""
    zxpm_switch_level: int = 1
    """群组插件开关管理对应权限"""
    zxpm_admin_default_auth: int = 5
    """群组管理员默认权限"""
    zxpm_font: str = "msyh.ttc"
    """字体"""
    zxpm_limit_superuser: bool = False
    """是否限制超管权限"""


ZxpmConfig = nonebot.get_plugin_config(Config)

if isinstance(ZxpmConfig.zxpm_data_path, str):
    ZxpmConfig.zxpm_data_path = Path(ZxpmConfig.zxpm_data_path)
ZxpmConfig.zxpm_data_path.mkdir(parents=True, exist_ok=True)
if ZxpmConfig.zxpm_db_url:
    if ZxpmConfig.zxpm_db_url.startswith("sqlite"):
        db_path = ZxpmConfig.zxpm_db_url.split(":")[-1]
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
else:
    db_path = ZxpmConfig.zxpm_data_path / "db" / "zxpm.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    ZxpmConfig.zxpm_db_url = f"sqlite:{db_path.absolute()!s}"
