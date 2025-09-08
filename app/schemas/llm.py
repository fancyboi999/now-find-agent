"""
LLM 相关 Schema 定义
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LLMBase(BaseModel):
    """LLM 基础模型"""
    
    provider: str = Field(..., max_length=256, description="LLM 提供商")
    model_name: str = Field(..., max_length=256, description="LLM 模型名称")
    model_type: str = Field(..., max_length=256, description="LLM 模型类型: 1-basic模型, 2-思考模型, 3-多模态模型")
    api_key: str = Field(..., max_length=256, description="LLM 模型 API Key")
    api_url: str = Field(..., max_length=256, description="LLM 模型 API URL")
    status: int = Field(..., description="LLM 模型状态")
    remark: Optional[str] = Field(None, max_length=256, description="备注")


class LLMCreate(LLMBase):
    """创建 LLM 模型"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "provider": "openai",
                "model_name": "gpt-4",
                "model_type": "1",
                "api_key": "sk-xxx...",
                "api_url": "https://api.openai.com/v1/chat/completions",
                "status": 1,
                "remark": "GPT-4 模型配置"
            }
        }


class LLMUpdate(BaseModel):
    """更新 LLM 模型"""
    
    provider: Optional[str] = Field(None, max_length=256, description="LLM 提供商")
    model_name: Optional[str] = Field(None, max_length=256, description="LLM 模型名称")
    model_type: Optional[str] = Field(None, max_length=256, description="LLM 模型类型")
    api_key: Optional[str] = Field(None, max_length=256, description="LLM 模型 API Key")
    api_url: Optional[str] = Field(None, max_length=256, description="LLM 模型 API URL")
    status: Optional[int] = Field(None, description="LLM 模型状态")
    remark: Optional[str] = Field(None, max_length=256, description="备注")


class LLMResponse(LLMBase):
    """LLM 响应模型"""
    
    id: int = Field(..., description="LLM ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "provider": "openai",
                "model_name": "gpt-4",
                "model_type": "1",
                "api_key": "sk-xxx...",
                "api_url": "https://api.openai.com/v1/chat/completions",
                "status": 1,
                "remark": "GPT-4 模型配置",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class LLMQuery(BaseModel):
    """LLM 查询模型"""
    
    id: Optional[int] = Field(None, description="LLM ID")
    provider: Optional[str] = Field(None, description="LLM 提供商")
    model_name: Optional[str] = Field(None, description="LLM 模型名称")
    model_type: Optional[str] = Field(None, description="LLM 模型类型")
    status: Optional[int] = Field(None, description="LLM 模型状态")
