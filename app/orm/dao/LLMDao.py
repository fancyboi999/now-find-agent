"""
LLM DAO 层
提供 LLM 相关的数据访问操作
"""

from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.LLM import LLM
from app.orm.dao.BaseDao import BaseDao


class LLMDao(BaseDao[LLM]):
    """LLM 数据访问对象"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, LLM)
    
    async def find_by_provider(self, provider: str) -> List[LLM]:
        """根据提供商查找 LLM 列表"""
        stmt = select(LLM).filter(LLM.provider == provider)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_by_model_name(self, model_name: str) -> Optional[LLM]:
        """根据模型名称查找 LLM"""
        stmt = select(LLM).filter(LLM.model_name == model_name)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    
    async def find_by_model_type(self, model_type: str) -> List[LLM]:
        """根据模型类型查找 LLM 列表"""
        stmt = select(LLM).filter(LLM.model_type == model_type)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_by_status(self, status: int) -> List[LLM]:
        """根据状态查找 LLM 列表"""
        stmt = select(LLM).filter(LLM.status == status)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def find_active_models(self) -> List[LLM]:
        """查找激活状态的 LLM 列表 (status=1)"""
        return await self.find_by_status(1)
    
    async def find_basic_models(self) -> List[LLM]:
        """查找基础模型列表 (model_type='1')"""
        return await self.find_by_model_type('1')
    
    async def find_thinking_models(self) -> List[LLM]:
        """查找思考模型列表 (model_type='2')"""
        return await self.find_by_model_type('2')
    
    async def find_multimodal_models(self) -> List[LLM]:
        """查找多模态模型列表 (model_type='3')"""
        return await self.find_by_model_type('3')
    
    async def search_models(
        self,
        keyword: Optional[str] = None,
        provider: Optional[str] = None,
        model_type: Optional[str] = None,
        status: Optional[int] = None
    ) -> List[LLM]:
        """多条件搜索 LLM"""
        stmt = select(LLM)
        conditions = []
        
        if keyword:
            # 在提供商、模型名称中搜索
            keyword_condition = or_(
                LLM.provider.ilike(f"%{keyword}%"),
                LLM.model_name.ilike(f"%{keyword}%")
            )
            conditions.append(keyword_condition)
        
        if provider:
            conditions.append(LLM.provider == provider)
        
        if model_type:
            conditions.append(LLM.model_type == model_type)
        
        if status is not None:
            conditions.append(LLM.status == status)
        
        if conditions:
            stmt = stmt.filter(and_(*conditions))
        
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def exists_by_model_name(self, model_name: str, exclude_id: Optional[int] = None) -> bool:
        """检查模型名称是否已存在（支持排除指定ID）"""
        stmt = select(LLM).filter(LLM.model_name == model_name)
        if exclude_id:
            stmt = stmt.filter(LLM.id != exclude_id)
        result = await self.db.execute(stmt)
        return result.scalars().first() is not None
    
    async def find_by_provider_and_type(self, provider: str, model_type: str) -> List[LLM]:
        """根据提供商和模型类型查找 LLM 列表"""
        stmt = select(LLM).filter(
            and_(LLM.provider == provider, LLM.model_type == model_type)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
