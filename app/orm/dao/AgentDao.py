"""
Agent DAO 层
提供 Agent 相关的数据访问操作
"""

from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.Agent import Agent
from app.orm.dao.BaseDao import BaseDao


class AgentDao(BaseDao[Agent]):
    """Agent 数据访问对象"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, Agent)
    
    async def find_by_name(self, name: str) -> Optional[Agent]:
        """根据名称查找 Agent"""
        stmt = select(Agent).filter(Agent.name == name)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def find_by_status(self, status: int) -> List[Agent]:
        """根据状态查找 Agent 列表"""
        stmt = select(Agent).filter(Agent.status == status)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_by_model_id(self, agent_model_id: int) -> List[Agent]:
        """根据模型ID查找 Agent 列表"""
        stmt = select(Agent).filter(Agent.agent_model_id == agent_model_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_by_level(self, level: int) -> List[Agent]:
        """根据级别查找 Agent 列表"""
        stmt = select(Agent).filter(Agent.level == level)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_optional_agents(self, is_optional: bool = True) -> List[Agent]:
        """查找可选/必选的 Agent 列表"""
        stmt = select(Agent).filter(Agent.is_optional == is_optional)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_active_agents(self) -> List[Agent]:
        """查找激活状态的 Agent 列表 (status=1)"""
        return await self.find_by_status(1)
    
    async def search_agents(
        self, 
        keyword: Optional[str] = None,
        status: Optional[int] = None,
        level: Optional[int] = None,
        agent_model_id: Optional[int] = None
    ) -> List[Agent]:
        """多条件搜索 Agent"""
        stmt = select(Agent)
        conditions = []
        
        if keyword:
            # 在名称、描述、中文名称中搜索
            keyword_condition = or_(
                Agent.name.ilike(f"%{keyword}%"),
                Agent.description.ilike(f"%{keyword}%"),
                Agent.zh_name.ilike(f"%{keyword}%")
            )
            conditions.append(keyword_condition)
        
        if status is not None:
            conditions.append(Agent.status == status)
        
        if level is not None:
            conditions.append(Agent.level == level)
        
        if agent_model_id is not None:
            conditions.append(Agent.agent_model_id == agent_model_id)
        
        if conditions:
            stmt = stmt.filter(and_(*conditions))
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """检查名称是否已存在（支持排除指定ID）"""
        stmt = select(Agent).filter(Agent.name == name)
        if exclude_id:
            stmt = stmt.filter(Agent.id != exclude_id)
        result = await self.db.execute(stmt)
        return result.scalars().first() is not None
