from pathlib import Path

import nonebot
from pydantic import BaseModel

DATA_PATH = Path() / "data" / "zxpm"
DB_FILE = DATA_PATH / "db" / "zxpm.db"

DEFAULT_DB_ULR = "sqlite:data/zxpm/db/zxpm.db"

DATA_PATH.mkdir(parents=True, exist_ok=True)
DB_FILE.parent.mkdir(parents=True, exist_ok=True)


class Config(BaseModel):
    zxpm_db_url: str | None = DEFAULT_DB_ULR
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


ZxpmConfig = nonebot.get_plugin_config(Config)
