# !/usr/bin/python3
"""
功能描述
----------------------------------------------------
@Project :   now-find-agent
@File    :   JsonUtil.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:17   zengxinmin@nowcoder.com   1.0         None
"""
import json


class JsonUtil:
    """
    JSON转换工具类
    """

    @staticmethod
    def object_to_json(obj, indent=None):
        """
        将对象转换为JSON字符串
        :param obj: 对象
        :param indent: 缩进
        :return: JSON字符串
        """
        return json.dumps(obj, default=lambda o: o.__dict__, indent=indent)

    @staticmethod
    def json_to_object(json_data, cls):
        """
        将JSON字符串转换为对象
        :param json_data: JSON字符串
        :return: 对象
        """
        return type(cls, object, **json.loads(json_data))


def dump_messages(messages):
    return json.dumps(
        [
            {
                "type": msg.__class__.__name__,
                "content": msg.content,
                "name": msg.name if hasattr(msg, "name") else None,
            }
            for msg in messages
        ],
        ensure_ascii=False,
        indent=2,
    )
