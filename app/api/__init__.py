"""
API 模块
统一管理应用的路由和接口定义
"""

from .example import router as example_router
from .health import router as health_router

__all__ = [
    "health_router",
    "example_router",
]
