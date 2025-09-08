"""
Agent API 路由
提供 Agent 相关的 REST API 接口
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.orm.service.AgentService import AgentService
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate
from app.schemas.base import DataResponseModel, PaginatedResponseModel

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/", response_model=DataResponseModel[AgentResponse], status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_create: AgentCreate,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[AgentResponse]:
    """创建新的 Agent"""
    try:
        agent_service = AgentService(db)
        agent = await agent_service.create_agent(agent_create)
        return DataResponseModel(
            data=AgentResponse.model_validate(agent),
            message="Agent 创建成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建 Agent 失败: {str(e)}"
        )


@router.get("/{agent_id}", response_model=DataResponseModel[AgentResponse])
async def get_agent(
    agent_id: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[AgentResponse]:
    """根据ID获取 Agent"""
    agent_service = AgentService(db)
    agent = await agent_service.get_agent_by_id(agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent ID {agent_id} 不存在"
        )
    
    return DataResponseModel(
        data=AgentResponse.model_validate(agent),
        message="获取 Agent 成功"
    )


@router.put("/{agent_id}", response_model=DataResponseModel[AgentResponse])
async def update_agent(
    agent_id: int,
    agent_update: AgentUpdate,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[AgentResponse]:
    """更新 Agent"""
    try:
        agent_service = AgentService(db)
        agent = await agent_service.update_agent(agent_id, agent_update)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent ID {agent_id} 不存在"
            )
        
        return DataResponseModel(
            data=AgentResponse.model_validate(agent),
            message="Agent 更新成功"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新 Agent 失败: {str(e)}"
        )


@router.delete("/{agent_id}", response_model=DataResponseModel[bool])
async def delete_agent(
    agent_id: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[bool]:
    """删除 Agent"""
    try:
        agent_service = AgentService(db)
        success = await agent_service.delete_agent(agent_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent ID {agent_id} 不存在"
            )
        
        return DataResponseModel(
            data=True,
            message="Agent 删除成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除 Agent 失败: {str(e)}"
        )


@router.get("/", response_model=DataResponseModel[List[AgentResponse]])
async def list_agents(
    status: Optional[int] = Query(None, description="过滤状态"),
    level: Optional[int] = Query(None, description="过滤级别"),
    agent_model_id: Optional[int] = Query(None, description="过滤模型ID"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    is_optional: Optional[bool] = Query(None, description="是否可选"),
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[AgentResponse]]:
    """获取 Agent 列表"""
    try:
        agent_service = AgentService(db)
        
        if keyword or status is not None or level is not None or agent_model_id is not None:
            # 条件搜索
            agents = await agent_service.search_agents(keyword, status, level, agent_model_id)
        elif is_optional is not None:
            # 按可选性筛选
            agents = await agent_service.get_optional_agents(is_optional)
        else:
            # 获取所有
            agents = await agent_service.get_all_agents()
        
        return DataResponseModel(
            data=[AgentResponse.model_validate(agent) for agent in agents],
            message=f"获取 Agent 列表成功，共 {len(agents)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 Agent 列表失败: {str(e)}"
        )


@router.get("/name/{name}", response_model=DataResponseModel[AgentResponse])
async def get_agent_by_name(
    name: str,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[AgentResponse]:
    """根据名称获取 Agent"""
    agent_service = AgentService(db)
    agent = await agent_service.get_agent_by_name(name)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent 名称 '{name}' 不存在"
        )
    
    return DataResponseModel(
        data=AgentResponse.model_validate(agent),
        message="获取 Agent 成功"
    )


@router.get("/active", response_model=DataResponseModel[List[AgentResponse]])
async def get_active_agents(
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[List[AgentResponse]]:
    """获取激活状态的 Agent 列表"""
    try:
        agent_service = AgentService(db)
        agents = await agent_service.get_active_agents()
        
        return DataResponseModel(
            data=[AgentResponse.model_validate(agent) for agent in agents],
            message=f"获取激活 Agent 列表成功，共 {len(agents)} 条记录"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取激活 Agent 列表失败: {str(e)}"
        )


@router.patch("/{agent_id}/status", response_model=DataResponseModel[AgentResponse])
async def update_agent_status(
    agent_id: int,
    new_status: int,
    db: AsyncSession = Depends(get_db)
) -> DataResponseModel[AgentResponse]:
    """更新 Agent 状态"""
    try:
        agent_service = AgentService(db)
        agent_update = AgentUpdate(status=new_status)
        agent = await agent_service.update_agent(agent_id, agent_update)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent ID {agent_id} 不存在"
            )
        
        return DataResponseModel(
            data=AgentResponse.model_validate(agent),
            message="Agent 状态更新成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新 Agent 状态失败: {str(e)}"
        )
