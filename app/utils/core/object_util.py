# !/usr/bin/python3
"""
对象工具类 - 提供对象操作相关的实用功能
----------------------------------------------------
@Project :   now-find-agent
@File    :   object_util.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2024/01/01 00:00   zengxinmin@nowcoder.com   1.0         对象工具类
"""
from typing import Any


class ObjectUtil:
    """对象工具类,提供对象操作相关的实用功能"""

    @staticmethod
    def is_none(obj: Any) -> bool:
        """
        判断对象是否为None

        Args:
            obj: 要判断的对象

        Returns:
            bool: 是否为None
        """
        return obj is None

    @staticmethod
    def is_not_none(obj: Any) -> bool:
        """
        判断对象是否不为None

        Args:
            obj: 要判断的对象

        Returns:
            bool: 是否不为None
        """
        return obj is not None

    @staticmethod
    def default_if_none(obj: Any, default_value: Any) -> Any:
        """
        如果对象为None则返回默认值

        Args:
            obj: 要判断的对象
            default_value: 默认值

        Returns:
            Any: 对象本身或默认值
        """
        return default_value if obj is None else obj

    @staticmethod
    def to_dict(obj: Any) -> dict[str, Any]:
        """
        将对象转换为字典

        Args:
            obj: 要转换的对象

        Returns:
            Dict[str, Any]: 转换后的字典
        """
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        elif isinstance(obj, dict):
            return obj
        else:
            return {}

    @staticmethod
    def copy_properties(
        source: Any, target: Any, exclude: list[str] | None = None
    ) -> None:
        """
        复制对象属性

        Args:
            source: 源对象
            target: 目标对象
            exclude: 要排除的属性列表
        """
        if exclude is None:
            exclude = []

        if hasattr(source, "__dict__"):
            for key, value in source.__dict__.items():
                if key not in exclude and hasattr(target, key):
                    setattr(target, key, value)

    @staticmethod
    def has_attribute(obj: Any, attr_name: str) -> bool:
        """
        判断对象是否有指定属性

        Args:
            obj: 对象
            attr_name: 属性名

        Returns:
            bool: 是否有指定属性
        """
        return hasattr(obj, attr_name)

    @staticmethod
    def get_attribute(obj: Any, attr_name: str, default_value: Any = None) -> Any:
        """
        获取对象属性值

        Args:
            obj: 对象
            attr_name: 属性名
            default_value: 默认值

        Returns:
            Any: 属性值或默认值
        """
        return getattr(obj, attr_name, default_value)
