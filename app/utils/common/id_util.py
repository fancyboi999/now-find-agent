"""
ID工具类
提供各种ID生成相关的工具方法
"""

import secrets
import string
import uuid


class IdUtil:
    """ID工具类,提供生成UUID等功能"""

    @staticmethod
    def generate_uuid() -> str:
        """
        生成标准UUID

        Returns:
            str: 标准格式UUID字符串,带连字符
        """
        return str(uuid.uuid4())

    @staticmethod
    def generate_uuid_32() -> str:
        """
        生成32位UUID(无连字符)

        Returns:
            str: 32位UUID字符串,不带连字符
        """
        return uuid.uuid4().hex

    @staticmethod
    def generate_call_id(prefix="call_", length=24):
        """
        生成一个唯一工具调用ID

        Args:
            prefix: 前缀字符串
            length: 生成的call_id长度
        """
        # Base62 字符集: [a-zA-Z0-9]
        alphabet = string.ascii_letters + string.digits
        unique_id = "".join(secrets.choice(alphabet) for _ in range(length))
        return f"{prefix}{unique_id}"
