"""
Agent Service 层
提供 Agent 相关的业务逻辑操作
"""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Agent import Agent
from app.orm.dao.AgentDao import AgentDao
from app.orm.service.BaseServiceImpl import BaseServiceImpl
from app.schemas.agent import AgentCreate, AgentUpdate, AgentQuery


class AgentService(BaseServiceImpl[Agent]):
    """Agent 业务服务类"""
    
    def __init__(self, db: AsyncSession):
        self.agent_dao = AgentDao(db)
        super().__init__(db, Agent, self.agent_dao)
    
    async def create_agent(self, agent_create: AgentCreate) -> Agent:
        """创建 Agent"""
        # 检查名称是否已存在
        if await self.agent_dao.exists_by_name(agent_create.name):
            raise ValueError(f"Agent 名称 '{agent_create.name}' 已存在")
        
        # 创建 Agent 实例
        agent = Agent(**agent_create.model_dump())
        return await self.agent_dao.save(agent)
    
    async def update_agent(self, agent_id: int, agent_update: AgentUpdate) -> Optional[Agent]:
        """更新 Agent"""
        # 查找现有 Agent
        agent = Agent(id=agent_id)
        existing_agent = await self.agent_dao.find_by_id(agent)
        if not existing_agent:
            return None
        
        # 检查名称唯一性（如果更新了名称）
        if agent_update.name and agent_update.name != existing_agent.name:
            if await self.agent_dao.exists_by_name(agent_update.name, exclude_id=agent_id):
                raise ValueError(f"Agent 名称 '{agent_update.name}' 已存在")
        
        # 更新字段
        update_data = agent_update.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_agent, field, value)
        
        # 手动刷新以获取更新后的字段值
        updated_agent = await self.agent_dao.update(existing_agent)
        await self.db.refresh(updated_agent)
        return updated_agent
    
    async def get_agent_by_id(self, agent_id: int) -> Optional[Agent]:
        """根据ID获取 Agent"""
        agent = Agent(id=agent_id)
        return await self.agent_dao.find_by_id(agent)
    
    async def get_agent_by_name(self, name: str) -> Optional[Agent]:
        """根据名称获取 Agent"""
        return await self.agent_dao.find_by_name(name)
    
    async def get_agents_by_status(self, status: int) -> List[Agent]:
        """根据状态获取 Agent 列表"""
        return await self.agent_dao.find_by_status(status)
    
    async def get_active_agents(self) -> List[Agent]:
        """获取激活状态的 Agent 列表"""
        return await self.agent_dao.find_active_agents()
    
    async def get_agents_by_model_id(self, agent_model_id: int) -> List[Agent]:
        """根据模型ID获取 Agent 列表"""
        return await self.agent_dao.find_by_model_id(agent_model_id)
    
    async def get_agents_by_level(self, level: int) -> List[Agent]:
        """根据级别获取 Agent 列表"""
        return await self.agent_dao.find_by_level(level)
    
    async def get_optional_agents(self, is_optional: bool = True) -> List[Agent]:
        """获取可选/必选的 Agent 列表"""
        return await self.agent_dao.find_optional_agents(is_optional)
    
    async def search_agents(
        self,
        keyword: Optional[str] = None,
        status: Optional[int] = None,
        level: Optional[int] = None,
        agent_model_id: Optional[int] = None
    ) -> List[Agent]:
        """多条件搜索 Agent"""
        return await self.agent_dao.search_agents(keyword, status, level, agent_model_id)
    
    async def delete_agent(self, agent_id: int) -> bool:
        """删除 Agent"""
        agent = Agent(id=agent_id)
        return await self.agent_dao.delete_by_id(agent)
    
    async def get_all_agents(self) -> List[Agent]:
        """获取所有 Agent"""
        agent_query = Agent()
        return await self.agent_dao.find_all(agent_query)
    
    async def agent_exists(self, name: str) -> bool:
        """检查 Agent 是否存在"""
        return await self.agent_dao.exists_by_name(name)
    
    async def batch_update_status(self, agent_ids: List[int], status: int) -> bool:
        """批量更新 Agent 状态"""
        agents = []
        for agent_id in agent_ids:
            agent = Agent(id=agent_id)
            existing_agent = await self.agent_dao.find_by_id(agent)
            if existing_agent:
                existing_agent.status = status
                agents.append(existing_agent)
        
        if agents:
            return await self.agent_dao.update_all(agents)
        return True
