"""
基础 Schema 定义
提供通用的 Pydantic 模型和响应结构
"""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')


class BaseResponseModel(BaseModel):
    """基础响应模型"""
    
    code: int = Field(default=200, description="响应状态码")
    message: str = Field(default="success", description="响应消息")
    success: bool = Field(default=True, description="请求是否成功")


class DataResponseModel(BaseResponseModel, Generic[T]):
    """带数据的响应模型"""
    
    data: Optional[T] = Field(default=None, description="响应数据")


class PaginationModel(BaseModel):
    """分页模型"""
    
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小")
    total: int = Field(default=0, ge=0, description="总记录数")
    pages: int = Field(default=0, ge=0, description="总页数")


class PaginatedResponseModel(BaseResponseModel, Generic[T]):
    """分页响应模型"""
    
    data: list[T] = Field(default_factory=list, description="数据列表")
    pagination: PaginationModel = Field(..., description="分页信息")


class HealthCheckModel(BaseModel):
    """健康检查模型"""
    
    status: str = Field(default="healthy", description="服务状态")
    timestamp: str = Field(..., description="检查时间")
    version: str = Field(default="1.0.0", description="服务版本")
    uptime: Optional[float] = Field(default=None, description="运行时间(秒)")


# 示例用户模型（可根据实际需求修改或删除）
class UserCreateModel(BaseModel):
    """用户创建模型"""
    
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: str = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=6, max_length=128, description="密码")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "secure_password123"
            }
        }


class UserResponseModel(BaseModel):
    """用户响应模型"""
    
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱地址")
    is_active: bool = Field(default=True, description="是否激活")
    created_at: str = Field(..., description="创建时间")
    updated_at: Optional[str] = Field(default=None, description="更新时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
