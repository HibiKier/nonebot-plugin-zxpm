import time
from collections import defaultdict
from datetime import datetime
from typing import Any

import pytz
from pydantic import BaseModel

from ..enum import BlockType, LimitWatchType, PluginLimitType


class BaseBlock(BaseModel):
    """
    插件阻断基本类（插件阻断限制）
    """

    status: bool = True
    """限制状态"""
    check_type: BlockType = BlockType.ALL
    """检查类型"""
    watch_type: LimitWatchType = LimitWatchType.USER
    """监听对象"""
    result: str | None = None
    """阻断时回复内容"""
    _type: PluginLimitType = PluginLimitType.BLOCK
    """类型"""


class PluginCdBlock(BaseBlock):
    """
    插件cd限制
    """

    cd: int = 5
    """cd"""
    _type: PluginLimitType = PluginLimitType.CD
    """类型"""


class PluginCountBlock(BaseBlock):
    """
    插件次数限制
    """

    max_count: int
    """最大调用次数"""
    _type: PluginLimitType = PluginLimitType.COUNT
    """类型"""


class CountLimiter:
    """
    每日调用命令次数限制
    """

    tz = pytz.timezone("Asia/Shanghai")

    def __init__(self, max_num):
        self.today = -1
        self.count = defaultdict(int)
        self.max = max_num

    def check(self, key) -> bool:
        day = datetime.now(self.tz).day
        if day != self.today:
            self.today = day
            self.count.clear()
        return self.count[key] < self.max

    def get_num(self, key):
        return self.count[key]

    def increase(self, key, num=1):
        self.count[key] += num

    def reset(self, key):
        self.count[key] = 0


class UserBlockLimiter:
    """
    检测用户是否正在调用命令
    """

    def __init__(self):
        self.flag_data = defaultdict(bool)
        self.time = time.time()

    def set_true(self, key: Any):
        self.time = time.time()
        self.flag_data[key] = True

    def set_false(self, key: Any):
        self.flag_data[key] = False

    def check(self, key: Any) -> bool:
        if time.time() - self.time > 30:
            self.set_false(key)
        return not self.flag_data[key]


class FreqLimiter:
    """
    命令冷却，检测用户是否处于冷却状态
    """

    def __init__(self, default_cd_seconds: int):
        self.next_time = defaultdict(float)
        self.default_cd = default_cd_seconds

    def check(self, key: Any) -> bool:
        return time.time() >= self.next_time[key]

    def start_cd(self, key: Any, cd_time: int = 0):
        self.next_time[key] = time.time() + (
            cd_time if cd_time > 0 else self.default_cd
        )

    def left_time(self, key: Any) -> float:
        return self.next_time[key] - time.time()
