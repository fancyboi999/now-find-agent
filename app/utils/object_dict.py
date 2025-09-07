# !/usr/bin/python3
"""
对象字典类 - 提供字典对象化访问功能
----------------------------------------------------
@Project :   now-find-agent
@File    :   object_dict.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2024/01/01 00:00   zengxinmin@nowcoder.com   1.0         对象字典类
"""
from typing import Any


class ObjectDict:
    """
    对象字典类,允许通过属性方式访问字典内容
    支持嵌套字典的对象化访问
    """

    def __init__(self, data: dict[str, Any] | None = None):
        """
        初始化ObjectDict

        Args:
            data: 初始字典数据
        """
        if data is None:
            data = {}
        self._data = {}
        for key, value in data.items():
            self._data[key] = self._convert_value(value)

    def _convert_value(self, value: Any) -> Any:
        """
        转换值,将嵌套字典转换为ObjectDict

        Args:
            value: 要转换的值

        Returns:
            Any: 转换后的值
        """
        if isinstance(value, dict):
            return ObjectDict(value)
        elif isinstance(value, list):
            return [self._convert_value(item) for item in value]
        return value

    def __getattr__(self, name: str) -> Any:
        """
        通过属性访问方式获取值

        Args:
            name: 属性名

        Returns:
            Any: 属性值

        Raises:
            AttributeError: 属性不存在时抛出
        """
        if name.startswith("_"):
            return super().__getattribute__(name)

        if name in self._data:
            return self._data[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __setattr__(self, name: str, value: Any) -> None:
        """
        通过属性设置方式设置值

        Args:
            name: 属性名
            value: 属性值
        """
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            if not hasattr(self, "_data"):
                super().__setattr__("_data", {})
            self._data[name] = self._convert_value(value)

    def __getitem__(self, key: str) -> Any:
        """
        通过字典访问方式获取值

        Args:
            key: 键名

        Returns:
            Any: 键值
        """
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """
        通过字典设置方式设置值

        Args:
            key: 键名
            value: 键值
        """
        self._data[key] = self._convert_value(value)

    def __contains__(self, key: str) -> bool:
        """
        判断是否包含指定键

        Args:
            key: 键名

        Returns:
            bool: 是否包含键
        """
        return key in self._data

    def __str__(self) -> str:
        """
        字符串表示

        Returns:
            str: 字符串表示
        """
        return str(self._data)

    def __repr__(self) -> str:
        """
        调试用字符串表示

        Returns:
            str: 调试字符串
        """
        return f"ObjectDict({self._data})"

    def to_dict(self) -> dict[str, Any]:
        """
        转换为普通字典

        Returns:
            Dict[str, Any]: 普通字典
        """
        result = {}
        for key, value in self._data.items():
            if isinstance(value, ObjectDict):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    item.to_dict() if isinstance(item, ObjectDict) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取值,支持默认值

        Args:
            key: 键名
            default: 默认值

        Returns:
            Any: 键值或默认值
        """
        return self._data.get(key, default)

    def keys(self):
        """
        获取所有键

        Returns:
            keys: 键的视图
        """
        return self._data.keys()

    def values(self):
        """
        获取所有值

        Returns:
            values: 值的视图
        """
        return self._data.values()

    def items(self):
        """
        获取所有键值对

        Returns:
            items: 键值对的视图
        """
        return self._data.items()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ObjectDict":
        """
        从字典创建ObjectDict实例

        Args:
            data: 字典数据

        Returns:
            ObjectDict: ObjectDict实例
        """
        return cls(data)

    @classmethod
    def from_json(cls, json_str: str) -> "ObjectDict":
        """
        从JSON字符串创建ObjectDict实例

        Args:
            json_str: JSON字符串

        Returns:
            ObjectDict: ObjectDict实例
        """
        import json

        data = json.loads(json_str)
        return cls(data)
