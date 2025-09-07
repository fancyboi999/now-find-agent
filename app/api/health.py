"""
健康检查 API
提供服务健康状态检查接口
"""

import time
from datetime import datetime

from fastapi import APIRouter

from app.schemas import DataResponseModel, HealthCheckModel

router = APIRouter(prefix="/health", tags=["健康检查"])

# 记录应用启动时间
_start_time = time.time()


@router.get("/", response_model=DataResponseModel[HealthCheckModel])
async def health_check():
    """
    健康检查接口
    
    返回服务的基本状态信息
    """
    uptime = time.time() - _start_time
    
    health_data = HealthCheckModel(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        uptime=uptime
    )
    
    return DataResponseModel(
        data=health_data,
        message="服务运行正常"
    )


@router.get("/live", response_model=DataResponseModel[dict])
async def liveness_probe():
    """
    存活性探针
    
    用于 Kubernetes 等容器编排系统的存活性检查
    """
    return DataResponseModel(
        data={"status": "alive"},
        message="服务存活"
    )


@router.get("/ready", response_model=DataResponseModel[dict])
async def readiness_probe():
    """
    就绪性探针
    
    检查服务是否已准备好接收流量
    """
    # 这里可以添加更复杂的就绪性检查逻辑
    # 例如：数据库连接、缓存连接等
    
    return DataResponseModel(
        data={"status": "ready"},
        message="服务就绪"
    )
