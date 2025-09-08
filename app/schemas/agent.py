"""
Agent 相关 Schema 定义
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AgentBase(BaseModel):
    """Agent 基础模型"""
    
    name: str = Field(..., min_length=1, max_length=256, description="Agent 名称")
    description: str = Field(..., min_length=1, max_length=256, description="Agent 描述")
    status: int = Field(..., description="Agent 状态")
    prompt: str = Field(..., min_length=1, max_length=10240, description="Agent 提示词")
    bind_tools_list: str = Field(..., max_length=256, description="绑定的工具列表")
    agent_model_id: int = Field(..., description="使用的 LLM 模型ID")
    zh_name: Optional[str] = Field(None, max_length=256, description="Agent 中文名称")
    is_optional: bool = Field(default=False, description="是否可选")
    level: int = Field(..., description="Agent 级别")
    remark: Optional[str] = Field(None, max_length=256, description="备注")


class AgentCreate(AgentBase):
    """创建 Agent 模型"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "data_analyst_agent",
                "description": "数据分析专家，帮助用户分析和解释数据",
                "status": 1,
                "prompt": "你是一个专业的数据分析师，能够帮助用户分析各种数据并提供洞察",
                "bind_tools_list": "chart_tool,excel_tool",
                "agent_model_id": 1,
                "zh_name": "数据分析专家",
                "is_optional": False,
                "level": 3,
                "remark": "适用于数据分析场景"
            }
        }


class AgentUpdate(BaseModel):
    """更新 Agent 模型"""
    
    name: Optional[str] = Field(None, min_length=1, max_length=256, description="Agent 名称")
    description: Optional[str] = Field(None, min_length=1, max_length=256, description="Agent 描述")
    status: Optional[int] = Field(None, description="Agent 状态")
    prompt: Optional[str] = Field(None, min_length=1, max_length=10240, description="Agent 提示词")
    bind_tools_list: Optional[str] = Field(None, max_length=256, description="绑定的工具列表")
    agent_model_id: Optional[int] = Field(None, description="使用的 LLM 模型ID")
    zh_name: Optional[str] = Field(None, max_length=256, description="Agent 中文名称")
    is_optional: Optional[bool] = Field(None, description="是否可选")
    level: Optional[int] = Field(None, description="Agent 级别")
    remark: Optional[str] = Field(None, max_length=256, description="备注")


class AgentResponse(AgentBase):
    """Agent 响应模型"""
    
    id: int = Field(..., description="Agent ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "data_analyst_agent",
                "description": "数据分析专家，帮助用户分析和解释数据",
                "status": 1,
                "prompt": "你是一个专业的数据分析师，能够帮助用户分析各种数据并提供洞察",
                "bind_tools_list": "chart_tool,excel_tool",
                "agent_model_id": 1,
                "zh_name": "数据分析专家",
                "is_optional": False,
                "level": 3,
                "remark": "适用于数据分析场景",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class AgentQuery(BaseModel):
    """Agent 查询模型"""
    
    id: Optional[int] = Field(None, description="Agent ID")
    name: Optional[str] = Field(None, description="Agent 名称")
    status: Optional[int] = Field(None, description="Agent 状态")
    agent_model_id: Optional[int] = Field(None, description="LLM 模型ID")
    is_optional: Optional[bool] = Field(None, description="是否可选")
    level: Optional[int] = Field(None, description="Agent 级别")
