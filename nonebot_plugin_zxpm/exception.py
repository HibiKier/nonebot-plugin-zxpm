class UserAndGroupIsNone(Exception):
    """
    用户/群组Id都为空
    """

    pass


class DbConnectError(Exception):
    """
    数据库连接错误
    """

    pass
