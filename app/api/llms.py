"""
LLM API 路由
提供 LLM 相关的 REST API 接口
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.orm.service.LLMService import LLMService
from app.schemas.llm import LLMCreate, LLMResponse, LLMUpdate
from app.schemas.base import DataResponseModel

router = APIRouter(prefix="/llms", tags=["llms"])


@router.post("/", response_model=DataResponseModel[LLMResponse], status_code=status.HTTP_201_CREATED)
async def create_llm(
    llm_create: LLMCreate,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[LLMResponse]:
    """创建新的 LLM"""
    try:
        llm_service = LLMService(db)
        llm = await llm_service.create_llm(llm_create)
        return DataResponseModel(
            data=LLMResponse.model_validate(llm),
            message="LLM 创建成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建 LLM 失败: {str(e)}"
        )


@router.get("/{llm_id}", response_model=DataResponseModel[LLMResponse])
async def get_llm(
    llm_id: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[LLMResponse]:
    """根据ID获取 LLM"""
    llm_service = LLMService(db)
    llm = await llm_service.get_llm_by_id(llm_id)
    
    if not llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM ID {llm_id} 不存在"
        )
    
    return DataResponseModel(
        data=LLMResponse.model_validate(llm),
        message="获取 LLM 成功"
    )


@router.put("/{llm_id}", response_model=DataResponseModel[LLMResponse])
async def update_llm(
    llm_id: int,
    llm_update: LLMUpdate,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[LLMResponse]:
    """更新 LLM"""
    try:
        llm_service = LLMService(db)
        llm = await llm_service.update_llm(llm_id, llm_update)
        
        if not llm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"LLM ID {llm_id} 不存在"
            )
        
        return DataResponseModel(
            data=LLMResponse.model_validate(llm),
            message="LLM 更新成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新 LLM 失败: {str(e)}"
        )


@router.delete("/{llm_id}", response_model=DataResponseModel[bool])
async def delete_llm(
    llm_id: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[bool]:
    """删除 LLM"""
    try:
        llm_service = LLMService(db)
        success = await llm_service.delete_llm(llm_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"LLM ID {llm_id} 不存在"
            )
        
        return DataResponseModel(
            data=True,
            message="LLM 删除成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除 LLM 失败: {str(e)}"
        )


@router.get("/", response_model=DataResponseModel[List[LLMResponse]])
async def list_llms(
    provider: Optional[str] = Query(None, description="过滤提供商"),
    model_type: Optional[str] = Query(None, description="过滤模型类型"),
    status: Optional[int] = Query(None, description="过滤状态"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[LLMResponse]]:
    """获取 LLM 列表"""
    try:
        llm_service = LLMService(db)
        
        if keyword or provider or model_type or status is not None:
            # 条件搜索
            llms = await llm_service.search_llms(keyword, provider, model_type, status)
        else:
            # 获取所有
            llms = await llm_service.get_all_llms()
        
        return DataResponseModel(
            data=[LLMResponse.model_validate(llm) for llm in llms],
            message=f"获取 LLM 列表成功，共 {len(llms)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 LLM 列表失败: {str(e)}"
        )


@router.get("/model-name/{model_name}", response_model=DataResponseModel[LLMResponse])
async def get_llm_by_model_name(
    model_name: str,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[LLMResponse]:
    """根据模型名称获取 LLM"""
    llm_service = LLMService(db)
    llm = await llm_service.get_llm_by_model_name(model_name)
    
    if not llm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"LLM 模型名称 '{model_name}' 不存在"
        )
    
    return DataResponseModel(
        data=LLMResponse.model_validate(llm),
        message="获取 LLM 成功"
    )


@router.get("/provider/{provider}", response_model=DataResponseModel[List[LLMResponse]])
async def get_llms_by_provider(
    provider: str,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[LLMResponse]]:
    """根据提供商获取 LLM 列表"""
    try:
        llm_service = LLMService(db)
        llms = await llm_service.get_llms_by_provider(provider)
        
        return DataResponseModel(
            data=[LLMResponse.model_validate(llm) for llm in llms],
            message=f"获取提供商 '{provider}' 的 LLM 列表成功，共 {len(llms)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 LLM 列表失败: {str(e)}"
        )


@router.get("/type/{model_type}", response_model=DataResponseModel[List[LLMResponse]])
async def get_llms_by_type(
    model_type: str,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[LLMResponse]]:
    """根据模型类型获取 LLM 列表"""
    try:
        llm_service = LLMService(db)
        llms = await llm_service.get_llms_by_type(model_type)
        
        return DataResponseModel(
            data=[LLMResponse.model_validate(llm) for llm in llms],
            message=f"获取类型 '{model_type}' 的 LLM 列表成功，共 {len(llms)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 LLM 列表失败: {str(e)}"
        )


@router.get("/active", response_model=DataResponseModel[List[LLMResponse]])
async def get_active_llms(
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[LLMResponse]]:
    """获取激活状态的 LLM 列表"""
    try:
        llm_service = LLMService(db)
        llms = await llm_service.get_active_llms()
        
        return DataResponseModel(
            data=[LLMResponse.model_validate(llm) for llm in llms],
            message=f"获取激活 LLM 列表成功，共 {len(llms)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取激活 LLM 列表失败: {str(e)}"
        )


@router.patch("/{llm_id}/status", response_model=DataResponseModel[LLMResponse])
async def update_llm_status(
    llm_id: int,
    new_status: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[LLMResponse]:
    """更新 LLM 状态"""
    try:
        llm_service = LLMService(db)
        llm_update = LLMUpdate(status=new_status)
        llm = await llm_service.update_llm(llm_id, llm_update)
        
        if not llm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"LLM ID {llm_id} 不存在"
            )
        
        return DataResponseModel(
            data=LLMResponse.model_validate(llm),
            message="LLM 状态更新成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新 LLM 状态失败: {str(e)}"
        )


@router.post("/{llm_id}/test", response_model=DataResponseModel[bool])
async def test_llm_connection(
    llm_id: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[bool]:
    """测试 LLM 连接"""
    try:
        llm_service = LLMService(db)
        success = await llm_service.test_llm_connection(llm_id)
        
        return DataResponseModel(
            data=success,
            message="LLM 连接测试完成" if success else "LLM 连接测试失败"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"测试 LLM 连接失败: {str(e)}"
        )
