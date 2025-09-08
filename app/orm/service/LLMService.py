"""
LLM Service 层
提供 LLM 相关的业务逻辑操作
"""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.LLM import LLM
from app.orm.dao.LLMDao import LLMDao
from app.orm.service.BaseServiceImpl import BaseServiceImpl
from app.schemas.llm import LLMCreate, LLMUpdate


class LLMService(BaseServiceImpl[LLM]):
    """LLM 业务服务类"""
    
    def __init__(self, db: AsyncSession):
        self.llm_dao = LLMDao(db)
        super().__init__(db, LLM, self.llm_dao)
    
    async def create_llm(self, llm_create: LLMCreate) -> LLM:
        """创建 LLM"""
        # 检查模型名称是否已存在
        if await self.llm_dao.exists_by_model_name(llm_create.model_name):
            raise ValueError(f"LLM 模型名称 '{llm_create.model_name}' 已存在")
        
        # 创建 LLM 实例
        llm = LLM(**llm_create.model_dump())
        return await self.llm_dao.save(llm)
    
    async def update_llm(self, llm_id: int, llm_update: LLMUpdate) -> Optional[LLM]:
        """更新 LLM"""
        # 查找现有 LLM
        llm = LLM(id=llm_id)
        existing_llm = await self.llm_dao.find_by_id(llm)
        if not existing_llm:
            return None
        
        # 检查模型名称唯一性（如果更新了模型名称）
        if llm_update.model_name and llm_update.model_name != existing_llm.model_name:
            if await self.llm_dao.exists_by_model_name(llm_update.model_name, exclude_id=llm_id):
                raise ValueError(f"LLM 模型名称 '{llm_update.model_name}' 已存在")
        
        # 更新字段
        update_data = llm_update.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_llm, field, value)
        
        # 手动刷新以获取更新后的字段值
        updated_llm = await self.llm_dao.update(existing_llm)
        await self.db.refresh(updated_llm)
        return updated_llm
    
    async def get_llm_by_id(self, llm_id: int) -> Optional[LLM]:
        """根据ID获取 LLM"""
        llm = LLM(id=llm_id)
        return await self.llm_dao.find_by_id(llm)
    
    async def get_llm_by_model_name(self, model_name: str) -> Optional[LLM]:
        """根据模型名称获取 LLM"""
        return await self.llm_dao.find_by_model_name(model_name)
    
    async def get_llms_by_provider(self, provider: str) -> List[LLM]:
        """根据提供商获取 LLM 列表"""
        return await self.llm_dao.find_by_provider(provider)
    
    async def get_llms_by_type(self, model_type: str) -> List[LLM]:
        """根据模型类型获取 LLM 列表"""
        return await self.llm_dao.find_by_model_type(model_type)
    
    async def get_llms_by_status(self, status: int) -> List[LLM]:
        """根据状态获取 LLM 列表"""
        return await self.llm_dao.find_by_status(status)
    
    async def get_active_llms(self) -> List[LLM]:
        """获取激活状态的 LLM 列表"""
        return await self.llm_dao.find_active_models()
    
    async def get_basic_models(self) -> List[LLM]:
        """获取基础模型列表"""
        return await self.llm_dao.find_basic_models()
    
    async def get_thinking_models(self) -> List[LLM]:
        """获取思考模型列表"""
        return await self.llm_dao.find_thinking_models()
    
    async def get_multimodal_models(self) -> List[LLM]:
        """获取多模态模型列表"""
        return await self.llm_dao.find_multimodal_models()
    
    async def search_llms(
        self,
        keyword: Optional[str] = None,
        provider: Optional[str] = None,
        model_type: Optional[str] = None,
        status: Optional[int] = None
    ) -> List[LLM]:
        """多条件搜索 LLM"""
        return await self.llm_dao.search_models(keyword, provider, model_type, status)
    
    async def delete_llm(self, llm_id: int) -> bool:
        """删除 LLM"""
        llm = LLM(id=llm_id)
        return await self.llm_dao.delete_by_id(llm)
    
    async def get_all_llms(self) -> List[LLM]:
        """获取所有 LLM"""
        llm_query = LLM()
        return await self.llm_dao.find_all(llm_query)
    
    async def llm_exists(self, model_name: str) -> bool:
        """检查 LLM 是否存在"""
        return await self.llm_dao.exists_by_model_name(model_name)
    
    async def get_llms_by_provider_and_type(self, provider: str, model_type: str) -> List[LLM]:
        """根据提供商和模型类型获取 LLM 列表"""
        return await self.llm_dao.find_by_provider_and_type(provider, model_type)
    
    async def batch_update_status(self, llm_ids: List[int], status: int) -> bool:
        """批量更新 LLM 状态"""
        llms = []
        for llm_id in llm_ids:
            llm = LLM(id=llm_id)
            existing_llm = await self.llm_dao.find_by_id(llm)
            if existing_llm:
                existing_llm.status = status
                llms.append(existing_llm)
        
        if llms:
            return await self.llm_dao.update_all(llms)
        return True
    
    async def test_llm_connection(self, llm_id: int) -> bool:
        """测试 LLM 连接（预留接口）"""
        # TODO: 实现实际的 LLM 连接测试逻辑
        llm = await self.get_llm_by_id(llm_id)
        if not llm:
            return False
        
        # 这里可以添加实际的 API 连接测试逻辑
        # 例如发送一个简单的请求测试 API 是否可用
        return True
