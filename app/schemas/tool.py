"""
Tool 相关 Schema 定义
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ToolBase(BaseModel):
    """Tool 基础模型"""
    
    name: str = Field(..., max_length=256, description="工具名称")
    description: str = Field(..., max_length=256, description="工具描述")
    tool_function: str = Field(..., max_length=256, description="工具对应程序函数")
    is_direct_return: bool = Field(default=False, description="是否直接返回结果")
    status: int = Field(..., description="工具状态")
    remark: Optional[str] = Field(None, max_length=256, description="备注")


class ToolCreate(ToolBase):
    """创建 Tool 模型"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "web_search",
                "description": "网络搜索工具，可以搜索互联网信息",
                "tool_function": "web_search_function",
                "is_direct_return": False,
                "status": 1,
                "remark": "基于搜索引擎的网络搜索工具"
            }
        }


class ToolUpdate(BaseModel):
    """更新 Tool 模型"""
    
    name: Optional[str] = Field(None, max_length=256, description="工具名称")
    description: Optional[str] = Field(None, max_length=256, description="工具描述")
    tool_function: Optional[str] = Field(None, max_length=256, description="工具对应程序函数")
    is_direct_return: Optional[bool] = Field(None, description="是否直接返回结果")
    status: Optional[int] = Field(None, description="工具状态")
    remark: Optional[str] = Field(None, max_length=256, description="备注")


class ToolResponse(ToolBase):
    """Tool 响应模型"""
    
    id: int = Field(..., description="Tool ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "web_search",
                "description": "网络搜索工具，可以搜索互联网信息",
                "tool_function": "web_search_function",
                "is_direct_return": False,
                "status": 1,
                "remark": "基于搜索引擎的网络搜索工具",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class ToolQuery(BaseModel):
    """Tool 查询模型"""
    
    id: Optional[int] = Field(None, description="Tool ID")
    name: Optional[str] = Field(None, description="工具名称")
    status: Optional[int] = Field(None, description="工具状态")
    is_direct_return: Optional[bool] = Field(None, description="是否直接返回结果")
