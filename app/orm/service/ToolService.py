"""
Tool Service 层
提供 Tool 相关的业务逻辑操作
"""

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Tool import Tool
from app.orm.dao.ToolDao import ToolDao
from app.orm.service.BaseServiceImpl import BaseServiceImpl
from app.schemas.tool import ToolCreate, ToolUpdate


class ToolService(BaseServiceImpl[Tool]):
    """Tool 业务服务类"""
    
    def __init__(self, db: AsyncSession):
        self.tool_dao = ToolDao(db)
        super().__init__(db, Tool, self.tool_dao)
    
    async def create_tool(self, tool_create: ToolCreate) -> Tool:
        """创建 Tool"""
        # 检查名称是否已存在
        if await self.tool_dao.exists_by_name(tool_create.name):
            raise ValueError(f"Tool 名称 '{tool_create.name}' 已存在")
        
        # 检查工具函数是否已存在
        if await self.tool_dao.exists_by_function(tool_create.tool_function):
            raise ValueError(f"Tool 函数 '{tool_create.tool_function}' 已存在")
        
        # 创建 Tool 实例
        tool = Tool(**tool_create.model_dump())
        return await self.tool_dao.save(tool)
    
    async def update_tool(self, tool_id: int, tool_update: ToolUpdate) -> Optional[Tool]:
        """更新 Tool"""
        # 查找现有 Tool
        tool = Tool(id=tool_id)
        existing_tool = await self.tool_dao.find_by_id(tool)
        if not existing_tool:
            return None
        
        # 检查名称唯一性（如果更新了名称）
        if tool_update.name and tool_update.name != existing_tool.name:
            if await self.tool_dao.exists_by_name(tool_update.name, exclude_id=tool_id):
                raise ValueError(f"Tool 名称 '{tool_update.name}' 已存在")
        
        # 检查工具函数唯一性（如果更新了工具函数）
        if tool_update.tool_function and tool_update.tool_function != existing_tool.tool_function:
            if await self.tool_dao.exists_by_function(tool_update.tool_function, exclude_id=tool_id):
                raise ValueError(f"Tool 函数 '{tool_update.tool_function}' 已存在")
        
        # 更新字段
        update_data = tool_update.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in update_data.items():
            setattr(existing_tool, field, value)
        
        # 手动刷新以获取更新后的字段值
        updated_tool = await self.tool_dao.update(existing_tool)
        await self.db.refresh(updated_tool)
        return updated_tool
    
    async def get_tool_by_id(self, tool_id: int) -> Optional[Tool]:
        """根据ID获取 Tool"""
        tool = Tool(id=tool_id)
        return await self.tool_dao.find_by_id(tool)
    
    async def get_tool_by_name(self, name: str) -> Optional[Tool]:
        """根据名称获取 Tool"""
        return await self.tool_dao.find_by_name(name)
    
    async def get_tool_by_function(self, tool_function: str) -> Optional[Tool]:
        """根据工具函数获取 Tool"""
        return await self.tool_dao.find_by_function(tool_function)
    
    async def get_tools_by_status(self, status: int) -> List[Tool]:
        """根据状态获取 Tool 列表"""
        return await self.tool_dao.find_by_status(status)
    
    async def get_active_tools(self) -> List[Tool]:
        """获取激活状态的 Tool 列表"""
        return await self.tool_dao.find_active_tools()
    
    async def get_direct_return_tools(self, is_direct_return: bool = True) -> List[Tool]:
        """获取直接返回/非直接返回的 Tool 列表"""
        return await self.tool_dao.find_direct_return_tools(is_direct_return)
    
    async def search_tools(
        self,
        keyword: Optional[str] = None,
        status: Optional[int] = None,
        is_direct_return: Optional[bool] = None
    ) -> List[Tool]:
        """多条件搜索 Tool"""
        return await self.tool_dao.search_tools(keyword, status, is_direct_return)
    
    async def delete_tool(self, tool_id: int) -> bool:
        """删除 Tool"""
        tool = Tool(id=tool_id)
        return await self.tool_dao.delete_by_id(tool)
    
    async def get_all_tools(self) -> List[Tool]:
        """获取所有 Tool"""
        tool_query = Tool()
        return await self.tool_dao.find_all(tool_query)
    
    async def tool_exists(self, name: str) -> bool:
        """检查 Tool 是否存在"""
        return await self.tool_dao.exists_by_name(name)
    
    async def tool_function_exists(self, tool_function: str) -> bool:
        """检查 Tool 函数是否存在"""
        return await self.tool_dao.exists_by_function(tool_function)
    
    async def get_tools_by_names(self, names: List[str]) -> List[Tool]:
        """根据名称列表获取 Tool 列表"""
        return await self.tool_dao.find_tools_by_names(names)
    
    async def get_tools_by_functions(self, functions: List[str]) -> List[Tool]:
        """根据函数列表获取 Tool 列表"""
        return await self.tool_dao.find_tools_by_functions(functions)
    
    async def batch_update_status(self, tool_ids: List[int], status: int) -> bool:
        """批量更新 Tool 状态"""
        tools = []
        for tool_id in tool_ids:
            tool = Tool(id=tool_id)
            existing_tool = await self.tool_dao.find_by_id(tool)
            if existing_tool:
                existing_tool.status = status
                tools.append(existing_tool)
        
        if tools:
            return await self.tool_dao.update_all(tools)
        return True
    
    async def validate_tool_config(self, tool_id: int) -> bool:
        """验证 Tool 配置（预留接口）"""
        # TODO: 实现实际的 Tool 配置验证逻辑
        tool = await self.get_tool_by_id(tool_id)
        if not tool:
            return False
        
        # 这里可以添加实际的工具配置验证逻辑
        # 例如检查工具函数是否存在、参数是否正确等
        return True
