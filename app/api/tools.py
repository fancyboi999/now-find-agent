"""
Tool API 路由
提供 Tool 相关的 REST API 接口
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.orm.service.ToolService import ToolService
from app.schemas.tool import ToolCreate, ToolResponse, ToolUpdate
from app.schemas.base import DataResponseModel

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/", response_model=DataResponseModel[ToolResponse], status_code=status.HTTP_201_CREATED)
async def create_tool(
    tool_create: ToolCreate,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[ToolResponse]:
    """创建新的 Tool"""
    try:
        tool_service = ToolService(db)
        tool = await tool_service.create_tool(tool_create)
        return DataResponseModel(
            data=ToolResponse.model_validate(tool),
            message="Tool 创建成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建 Tool 失败: {str(e)}"
        )


@router.get("/{tool_id}", response_model=DataResponseModel[ToolResponse])
async def get_tool(
    tool_id: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[ToolResponse]:
    """根据ID获取 Tool"""
    tool_service = ToolService(db)
    tool = await tool_service.get_tool_by_id(tool_id)
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool ID {tool_id} 不存在"
        )
    
    return DataResponseModel(
        data=ToolResponse.model_validate(tool),
        message="获取 Tool 成功"
    )


@router.put("/{tool_id}", response_model=DataResponseModel[ToolResponse])
async def update_tool(
    tool_id: int,
    tool_update: ToolUpdate,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[ToolResponse]:
    """更新 Tool"""
    try:
        tool_service = ToolService(db)
        tool = await tool_service.update_tool(tool_id, tool_update)
        
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool ID {tool_id} 不存在"
            )
        
        return DataResponseModel(
            data=ToolResponse.model_validate(tool),
            message="Tool 更新成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新 Tool 失败: {str(e)}"
        )


@router.delete("/{tool_id}", response_model=DataResponseModel[bool])
async def delete_tool(
    tool_id: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[bool]:
    """删除 Tool"""
    try:
        tool_service = ToolService(db)
        success = await tool_service.delete_tool(tool_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool ID {tool_id} 不存在"
            )
        
        return DataResponseModel(
            data=True,
            message="Tool 删除成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除 Tool 失败: {str(e)}"
        )


@router.get("/", response_model=DataResponseModel[List[ToolResponse]])
async def list_tools(
    status: Optional[int] = Query(None, description="过滤状态"),
    is_direct_return: Optional[bool] = Query(None, description="是否直接返回"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[ToolResponse]]:
    """获取 Tool 列表"""
    try:
        tool_service = ToolService(db)
        
        if keyword or status is not None or is_direct_return is not None:
            # 条件搜索
            tools = await tool_service.search_tools(keyword, status, is_direct_return)
        else:
            # 获取所有
            tools = await tool_service.get_all_tools()
        
        return DataResponseModel(
            data=[ToolResponse.model_validate(tool) for tool in tools],
            message=f"获取 Tool 列表成功，共 {len(tools)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 Tool 列表失败: {str(e)}"
        )


@router.get("/name/{name}", response_model=DataResponseModel[ToolResponse])
async def get_tool_by_name(
    name: str,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[ToolResponse]:
    """根据名称获取 Tool"""
    tool_service = ToolService(db)
    tool = await tool_service.get_tool_by_name(name)
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool 名称 '{name}' 不存在"
        )
    
    return DataResponseModel(
        data=ToolResponse.model_validate(tool),
        message="获取 Tool 成功"
    )


@router.get("/function/{tool_function}", response_model=DataResponseModel[ToolResponse])
async def get_tool_by_function(
    tool_function: str,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[ToolResponse]:
    """根据工具函数获取 Tool"""
    tool_service = ToolService(db)
    tool = await tool_service.get_tool_by_function(tool_function)
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool 函数 '{tool_function}' 不存在"
        )
    
    return DataResponseModel(
        data=ToolResponse.model_validate(tool),
        message="获取 Tool 成功"
    )


@router.get("/active", response_model=DataResponseModel[List[ToolResponse]])
async def get_active_tools(
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[ToolResponse]]:
    """获取激活状态的 Tool 列表"""
    try:
        tool_service = ToolService(db)
        tools = await tool_service.get_active_tools()
        
        return DataResponseModel(
            data=[ToolResponse.model_validate(tool) for tool in tools],
            message=f"获取激活 Tool 列表成功，共 {len(tools)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取激活 Tool 列表失败: {str(e)}"
        )


@router.get("/direct-return", response_model=DataResponseModel[List[ToolResponse]])
async def get_direct_return_tools(
    is_direct: bool = Query(True, description="是否直接返回"),
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[ToolResponse]]:
    """获取直接返回/非直接返回的 Tool 列表"""
    try:
        tool_service = ToolService(db)
        tools = await tool_service.get_direct_return_tools(is_direct)
        
        return DataResponseModel(
            data=[ToolResponse.model_validate(tool) for tool in tools],
            message=f"获取{'直接返回' if is_direct else '非直接返回'} Tool 列表成功，共 {len(tools)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 Tool 列表失败: {str(e)}"
        )


@router.patch("/{tool_id}/status", response_model=DataResponseModel[ToolResponse])
async def update_tool_status(
    tool_id: int,
    new_status: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[ToolResponse]:
    """更新 Tool 状态"""
    try:
        tool_service = ToolService(db)
        tool_update = ToolUpdate(status=new_status)
        tool = await tool_service.update_tool(tool_id, tool_update)
        
        if not tool:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool ID {tool_id} 不存在"
            )
        
        return DataResponseModel(
            data=ToolResponse.model_validate(tool),
            message="Tool 状态更新成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新 Tool 状态失败: {str(e)}"
        )


@router.post("/{tool_id}/validate", response_model=DataResponseModel[bool])
async def validate_tool_config(
    tool_id: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[bool]:
    """验证 Tool 配置"""
    try:
        tool_service = ToolService(db)
        success = await tool_service.validate_tool_config(tool_id)
        
        return DataResponseModel(
            data=success,
            message="Tool 配置验证完成" if success else "Tool 配置验证失败"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"验证 Tool 配置失败: {str(e)}"
        )


@router.post("/batch/names", response_model=DataResponseModel[List[ToolResponse]])
async def get_tools_by_names(
    names: List[str],
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[ToolResponse]]:
    """根据名称列表批量获取 Tool"""
    try:
        tool_service = ToolService(db)
        tools = await tool_service.get_tools_by_names(names)
        
        return DataResponseModel(
            data=[ToolResponse.model_validate(tool) for tool in tools],
            message=f"批量获取 Tool 成功，共 {len(tools)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量获取 Tool 失败: {str(e)}"
        )
