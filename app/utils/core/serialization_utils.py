import asyncio
from typing import Any

from loguru import logger


async def async_safe_serialize(obj: Any) -> str | dict | list | None:
    """安全地异步序列化对象,处理异常情况

    Args:
        obj: 要序列化的对象

    Returns:
        序列化后的对象或字符串
    """
    if obj is None:
        return None

    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, safe_serialize_inner, obj)
    except Exception as e:
        logger.error(f"异步序列化对象时出错: {e!s}")
        return str(obj)


def safe_serialize_inner(obj: Any) -> str | dict | list | None:
    """内部同步序列化函数,由异步函数调用"""
    if obj is None:
        return None

    try:
        if isinstance(obj, dict | list):
            return obj
        elif hasattr(obj, "content"):
            return obj.content
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return str(obj)
    except Exception as e:
        logger.error(f"序列化对象时出错: {e!s}")
        return str(obj)


def safe_serialize_simple(obj: Any) -> str | dict | list | None:
    """简化版的序列化函数,优化性能

    Args:
        obj: 要序列化的对象

    Returns:
        序列化后的对象
    """
    if obj is None:
        return None

    try:
        if isinstance(obj, str | int | float | bool):
            return obj
        elif isinstance(obj, dict | list):
            return obj
        elif hasattr(obj, "content"):
            return obj.content
        elif hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()
        else:
            return str(obj)
    except Exception as e:
        logger.error(f"简化序列化对象时出错: {e!s}")
        return str(obj)
