"""
FastAPI 依赖注入
提供数据库会话等公共依赖
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.providers.database import get_engine


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取异步数据库会话
    
    Yields:
        AsyncSession: 异步数据库会话
    """
    _, async_session = get_engine()
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
