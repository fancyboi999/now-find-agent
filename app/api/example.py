"""
示例 API
展示如何使用脚手架进行 API 开发
"""

# 导入必要的模块
from fastapi import APIRouter, HTTPException, Query

from app.constants import HTTPStatus, ResponseMessage
from app.schemas import (BaseResponseModel, DataResponseModel,
                         PaginatedResponseModel, PaginationModel,
                         UserCreateModel, UserResponseModel)

router = APIRouter(prefix="/example", tags=["示例接口"])

# 模拟数据存储
_users_db = []
_next_id = 1


@router.get("/", response_model=BaseResponseModel)
async def example_root():
    """
    示例根接口
    """
    return BaseResponseModel(
        message="这是一个示例API接口"
    )


@router.post("/users", response_model=DataResponseModel[UserResponseModel])
async def create_user(user_data: UserCreateModel):
    """
    创建用户示例
    
    展示如何创建资源的标准做法
    """
    global _next_id
    
    # 检查用户名是否已存在
    for user in _users_db:
        if user["username"] == user_data.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="用户名已存在"
            )
    
    # 创建新用户
    new_user = {
        "id": _next_id,
        "username": user_data.username,
        "email": user_data.email,
        "is_active": True,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
    
    _users_db.append(new_user)
    _next_id += 1
    
    return DataResponseModel(
        code=HTTPStatus.CREATED,
        data=UserResponseModel(**new_user),
        message=ResponseMessage.CREATED
    )


@router.get("/users", response_model=PaginatedResponseModel[UserResponseModel])
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页大小")
):
    """
    获取用户列表示例
    
    展示分页查询的标准做法
    """
    # 计算分页
    total = len(_users_db)
    offset = (page - 1) * page_size
    users = _users_db[offset:offset + page_size]
    
    # 转换为响应模型
    user_responses = [UserResponseModel(**user) for user in users]
    
    pagination = PaginationModel(
        page=page,
        page_size=page_size,
        total=total,
        pages=(total + page_size - 1) // page_size
    )
    
    return PaginatedResponseModel(
        data=user_responses,
        pagination=pagination,
        message=ResponseMessage.SUCCESS
    )


@router.get("/users/{user_id}", response_model=DataResponseModel[UserResponseModel])
async def get_user(user_id: int):
    """
    获取单个用户示例
    
    展示如何获取特定资源
    """
    for user in _users_db:
        if user["id"] == user_id:
            return DataResponseModel(
                data=UserResponseModel(**user),
                message=ResponseMessage.SUCCESS
            )
    
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=ResponseMessage.NOT_FOUND
    )


@router.delete("/users/{user_id}", response_model=BaseResponseModel)
async def delete_user(user_id: int):
    """
    删除用户示例
    
    展示如何删除资源
    """
    for i, user in enumerate(_users_db):
        if user["id"] == user_id:
            _users_db.pop(i)
            return BaseResponseModel(
                message=ResponseMessage.DELETED
            )
    
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=ResponseMessage.NOT_FOUND
    )
