"""
Tool DAO 层
提供 Tool 相关的数据访问操作
"""

from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.Tool import Tool
from app.orm.dao.BaseDao import BaseDao


class ToolDao(BaseDao[Tool]):
    """Tool 数据访问对象"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Tool)
    
    async def find_by_name(self, name: str) -> Optional[Tool]:
        """根据名称查找 Tool"""
        stmt = select(Tool).filter(Tool.name == name)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def find_by_function(self, tool_function: str) -> Optional[Tool]:
        """根据工具函数查找 Tool"""
        stmt = select(Tool).filter(Tool.tool_function == tool_function)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def find_by_status(self, status: int) -> List[Tool]:
        """根据状态查找 Tool 列表"""
        stmt = select(Tool).filter(Tool.status == status)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_direct_return_tools(self, is_direct_return: bool = True) -> List[Tool]:
        """查找直接返回/非直接返回的 Tool 列表"""
        stmt = select(Tool).filter(Tool.is_direct_return == is_direct_return)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_active_tools(self) -> List[Tool]:
        """查找激活状态的 Tool 列表 (status=1)"""
        return await self.find_by_status(1)
    
    async def search_tools(
        self,
        keyword: Optional[str] = None,
        status: Optional[int] = None,
        is_direct_return: Optional[bool] = None
    ) -> List[Tool]:
        """多条件搜索 Tool"""
        stmt = select(Tool)
        conditions = []
        
        if keyword:
            # 在名称、描述、工具函数中搜索
            keyword_condition = or_(
                Tool.name.ilike(f"%{keyword}%"),
                Tool.description.ilike(f"%{keyword}%"),
                Tool.tool_function.ilike(f"%{keyword}%")
            )
            conditions.append(keyword_condition)
        
        if status is not None:
            conditions.append(Tool.status == status)
        
        if is_direct_return is not None:
            conditions.append(Tool.is_direct_return == is_direct_return)
        
        if conditions:
            stmt = stmt.filter(and_(*conditions))
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """检查名称是否已存在（支持排除指定ID）"""
        stmt = select(Tool).filter(Tool.name == name)
        if exclude_id:
            stmt = stmt.filter(Tool.id != exclude_id)
        result = await self.db.execute(stmt)
        return result.scalars().first() is not None
    
    async def exists_by_function(self, tool_function: str, exclude_id: Optional[int] = None) -> bool:
        """检查工具函数是否已存在（支持排除指定ID）"""
        stmt = select(Tool).filter(Tool.tool_function == tool_function)
        if exclude_id:
            stmt = stmt.filter(Tool.id != exclude_id)
        result = await self.db.execute(stmt)
        return result.scalars().first() is not None
    
    async def find_tools_by_names(self, names: List[str]) -> List[Tool]:
        """根据名称列表查找 Tool 列表"""
        stmt = select(Tool).filter(Tool.name.in_(names))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_tools_by_functions(self, functions: List[str]) -> List[Tool]:
        """根据函数列表查找 Tool 列表"""
        stmt = select(Tool).filter(Tool.tool_function.in_(functions))
        result = await self.db.execute(stmt)
        return result.scalars().all()
