from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from redis.asyncio import from_url

from app.models.BaseModels import Base  # 创建表的关键
from app.providers.database import (
    SCHEMA_NAME,
    check_database_health, 
    engine,
    get_database_pool_status
)
from config.config import DevelopmentSettings, ProductionSettings, get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI应用生命周期管理
    
    脚手架版本 - 提供基础的数据库、Redis连接管理
    
    before yield: 服务器启动前的初始化操作
    after yield: 服务器关闭后的清理操作
    
    Args:
        app (FastAPI): FastAPI应用实例
    """
    logger.info("Application starting...")
    logger.info(f"使用数据库Schema: {SCHEMA_NAME}")

    # 初始化全局任务字典 - 用于存储异步任务实例
    app.task_dict = {}  # type: ignore

    # 初始化Redis连接
    redis_url = (
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    )
    if settings.REDIS_PASSWORD:
        redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"

    app.redis = from_url(  # type: ignore
        redis_url,
        encoding="utf-8",
        decode_responses=True,  # 解码为字符串而非bytes
    )

    # 检查主数据库连接健康状态
    logger.info("正在检查数据库连接健康状态...")
    db_healthy = await check_database_health()
    if db_healthy:
        logger.info("数据库连接健康检查通过")
        # 获取连接池状态信息
        pool_status = await get_database_pool_status()
        if pool_status:
            logger.info(f"数据库连接池状态: {pool_status}")
    else:
        logger.error("数据库连接健康检查失败,但应用将继续启动")

    # 检查并创建数据库表结构
    try:
        async with engine.begin() as conn:
            await conn.run_sync(
                Base.metadata.create_all
            )  # 检查数据库中是否存在相应的表, 如不存在则创建
        logger.info("数据库表结构检查完成")
    except Exception as e:
        logger.error(f"数据库表结构检查失败: {e}")

    # TODO: 在此处添加您的业务初始化逻辑
    # 例如: 初始化缓存、加载配置、启动后台任务等
    
    logger.info("应用启动完成,开始提供服务")
    
    # 应用启动完成,开始提供服务
    yield

    # ===== 应用关闭时的清理工作 =====
    logger.info("Application shutting down...")

    # 清理数据库连接
    try:
        await engine.dispose()
        logger.info("数据库连接已关闭")
    except Exception as e:
        logger.error(f"关闭数据库连接失败: {e}")

    # 清理Redis连接
    try:
        app.redis.close()  # type: ignore
        logger.info("Redis连接已关闭")
    except Exception as e:
        logger.error(f"关闭Redis连接失败: {e}")

    # TODO: 在此处添加您的业务清理逻辑
    # 例如: 关闭后台任务、清理缓存、保存状态等

    logger.info("Application stopped.")


def add_global_middleware(app: FastAPI, app_settings):
    """注册全局中间件
    
    脚手架版本 - 提供基础的CORS和请求日志中间件
    可根据业务需求添加更多中间件
    """
    # 导入请求日志中间件
    from app.http.middleware.request_logger import RequestLoggerMiddleware
    
    # app_settings 参数预留给将来的中间件配置使用
    _ = app_settings  # 避免 unused argument 警告

    # 注册CORS中间件 - 处理跨域请求
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许的来源 - 生产环境建议限制具体域名
        allow_credentials=True,  # 允许携带 Cookie
        allow_methods=["*"],  # 允许的请求方法(GET, POST等)
        allow_headers=["*"],  # 允许的请求头
    )

    # 注册请求日志中间件 - 记录API请求日志
    app.add_middleware(RequestLoggerMiddleware)

    # TODO: 在此处添加您的自定义中间件
    # 例如: 认证中间件、限流中间件、安全中间件等


def register(app: FastAPI, app_settings: DevelopmentSettings | ProductionSettings):
    """注册应用配置和中间件
    
    Args:
        app: FastAPI应用实例
        app_settings: 应用配置
    """
    app.debug = app_settings.DEBUG
    app.title = app_settings.NAME

    # 注册全局中间件
    add_global_middleware(app, app_settings)
