"""
应用配置管理
基于环境变量的分层配置系统
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """基础配置类"""
    
    # 应用基础配置
    NAME: str = Field(default="FastAPI App", description="应用名称")
    ENV: str = Field(default="dev", description="环境名称")
    
    # 服务器配置
    SERVER_HOST: str = Field(default="0.0.0.0", description="服务器地址")
    SERVER_PORT: int = Field(default=8000, description="服务器端口")
    DEBUG: bool = Field(default=False, description="调试模式")
    WORKERS: int = Field(default=1, description="工作进程数")
    
    # Uvicorn配置
    UVICORN_TIMEOUT_KEEP_ALIVE: int = Field(default=5, description="Keep-alive超时时间")
    UVICORN_GRACEFUL_TIMEOUT: int = Field(default=5, description="优雅关闭超时时间")
    PROXY_HEADERS: bool = Field(default=True, description="代理头部")
    FORWARDED_ALLOW_IPS: str = Field(default="*", description="允许的转发IP")
    
    # 数据库配置
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description="数据库连接URL(异步)"
    )
    DATABASE_URL_SYNC: Optional[str] = Field(
        default=None,
        description="同步数据库连接URL(JDBC格式)"
    )
    DATABASE_USERNAME: Optional[str] = Field(default="nc_test", description="数据库用户名")
    DATABASE_PASSWORD: Optional[str] = Field(default="nc_test_2019", description="数据库密码")
    
    # Redis配置
    REDIS_URL: Optional[str] = Field(default=None, description="Redis连接URL")
    REDIS_HOST: str = Field(default="localhost", description="Redis主机地址")
    REDIS_PORT: int = Field(default=6379, description="Redis端口")
    REDIS_DB: int = Field(default=0, description="Redis数据库编号")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis密码")

    # 前端配置
    FRONTEND_URL: str = Field(default="http://localhost:3000", description="前端应用地址")
    
    # 日志配置
    LOG_LEVEL: str = Field(default="INFO", description="日志级别")
    LOG_LEVEL_ERROR: str = Field(default="ERROR", description="错误日志级别")
    LOG_PATH: str = Field(default="config/settings/storage/logs/fastapi-{{time:YYYY-MM-DD}}.log", description="日志文件路径")
    LOG_PATH_ERROR: str = Field(default="config/settings/storage/logs/error/fastapi-{{time:YYYY-MM-DD}}.log", description="错误日志文件路径")
    LOG_ROTATION: str = Field(default="00:00", description="日志轮转时间")
    LOG_RETENTION: str = Field(default="7 days", description="日志保留时间")
    
    # JWT配置
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", description="JWT密钥")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="访问令牌过期时间(分钟)")
    
    # 加密密钥配置
    PUBLIC_KEY_CLIENT: Optional[str] = Field(default=None, description="客户端公钥")
    PRIVATE_KEY_SERVER: Optional[str] = Field(default=None, description="服务器私钥")
    
    # 第三方服务配置
    FIRECRAWL_KEY: Optional[str] = Field(default=None, description="Firecrawl API密钥")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


class DevelopmentSettings(BaseAppSettings):
    """开发环境配置"""
    
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    WORKERS: int = 1
    
    class Config:
        env_file = [".env", ".env.dev"]
        case_sensitive = True


class ProductionSettings(BaseAppSettings):
    """生产环境配置"""
    
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    WORKERS: int = 4
    
    class Config:
        env_file = [".env", ".env.prod"]
        case_sensitive = True


class TestSettings(BaseAppSettings):
    """测试环境配置"""
    
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    
    class Config:
        env_file = [".env", ".env.test"]
        case_sensitive = True


class UATSettings(BaseAppSettings):
    """UAT用户验收测试环境配置"""
    
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    WORKERS: int = 2
    
    class Config:
        env_file = [".env", ".env.uat"]
        case_sensitive = True


@lru_cache()
def get_settings() -> BaseAppSettings:
    """
    获取配置实例
    根据DEPLOY_ENV环境变量返回对应的配置
    
    支持的环境:
    - dev/development: 开发环境
    - test/testing: 测试环境
    - uat: UAT用户验收测试环境
    - prod/production: 生产环境
    """
    env = os.getenv("DEPLOY_ENV", "dev").lower()
    
    if env in ["development", "dev"]:
        return DevelopmentSettings()
    elif env in ["test", "testing"]:
        return TestSettings()
    elif env in ["uat", "user-acceptance-test"]:
        return UATSettings()
    elif env in ["production", "prod"]:
        return ProductionSettings()
    else:
        return DevelopmentSettings()  # 默认开发环境
