"""
应用配置管理
基于环境变量和Nacos配置中心的分层配置系统
"""

import os
import asyncio
from functools import lru_cache
from typing import Optional, Dict, Any

from pydantic import Field
from pydantic_settings import BaseSettings
from loguru import logger

from .nacos import NacosConfigManager, NacosSettings
from .secure_config import get_secure_config_manager


class BaseAppSettings(BaseSettings):
    """基础配置类"""
    
    # 应用基础配置
    NAME: str = Field(default="FastAPI App", description="应用名称")
    ENV: str = Field(default="dev", description="环境名称")
    DEPLOY_ENV: str = Field(default="dev", description="部署环境")
    
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
    
    # Nacos配置中心设置
    USE_NACOS: bool = Field(default=True, description="是否使用Nacos配置中心")
    NACOS_SERVER: Optional[str] = Field(default=None, description="Nacos服务器地址")
    NACOS_NAMESPACE: Optional[str] = Field(default=None, description="Nacos命名空间")
    NACOS_GROUP: Optional[str] = Field(default=None, description="Nacos分组")
    NACOS_ACCESS_KEY: Optional[str] = Field(default=None, description="Nacos访问密钥")
    NACOS_SECRET_KEY: Optional[str] = Field(default=None, description="Nacos密钥")
    NACOS_TIMEOUT: int = Field(default=30, description="Nacos连接超时时间")
    NACOS_MAX_RETRY: int = Field(default=3, description="Nacos最大重试次数")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._nacos_manager: Optional[NacosConfigManager] = None
        self._nacos_config: Dict[str, Any] = {}
    
    async def initialize_nacos(self):
        """初始化Nacos配置中心"""
        # 初始化安全配置管理器
        secure_manager = get_secure_config_manager()
        
        if not self.USE_NACOS:
            logger.info("Nacos configuration center disabled, using secure local configuration")
            # 在开发环境加载安全配置
            if self.ENV == "dev":
                secure_manager.load_development_config()
                secure_manager.log_config_summary()
            return
        
        try:
            # 创建Nacos管理器
            nacos_settings = NacosSettings()
            self._nacos_manager = NacosConfigManager(nacos_settings)
            
            # 初始化客户端
            initialized = await self._nacos_manager.initialize()
            if initialized:
                # 加载配置
                self._nacos_config = await self._nacos_manager.load_all_configs(self.ENV)
                
                # 如果Nacos配置为空，使用安全本地配置
                if not self._nacos_config.get("database") and self.ENV == "dev":
                    logger.info("Nacos configuration empty, using secure local configuration")
                    secure_manager.load_development_config()
                    
                    # 应用本地配置
                    self.DATABASE_URL = secure_manager.build_database_url()
                    self.REDIS_URL = secure_manager.build_redis_url()
                    
                    # 设置第三方服务配置
                    tencent_config = secure_manager.get_tencent_asr_config()
                    sparta_config = secure_manager.get_sparta_job_config()
                    
                    if tencent_config["secret_id"]:
                        os.environ["TENCENT_ASR_SECRET_ID"] = tencent_config["secret_id"]
                        os.environ["TENCENT_ASR_SECRET_KEY"] = tencent_config["secret_key"]
                    
                    if sparta_config["address"]:
                        os.environ["SPARTA_JOB_ADDRESS"] = sparta_config["address"]
                        os.environ["SPARTA_JOB_TOKEN"] = sparta_config["token"]
                    
                    secure_manager.log_config_summary()
                else:
                    # 应用Nacos配置
                    await self._apply_nacos_config()
                
                logger.info("Configuration initialized successfully")
            else:
                logger.warning("Failed to initialize Nacos, using secure local configuration")
                if self.ENV == "dev":
                    secure_manager.load_development_config()
                    secure_manager.log_config_summary()
                
        except Exception as e:
            logger.error(f"Error initializing configuration: {e}")
            # 降级到安全本地配置
            if self.ENV == "dev":
                secure_manager.load_development_config()
                secure_manager.log_config_summary()
    
    async def _apply_nacos_config(self):
        """应用Nacos配置"""
        if not self._nacos_config:
            return
        
        # 应用数据库配置
        if "database" in self._nacos_config:
            db_config = self._nacos_config["database"]
            if "url" in db_config:
                self.DATABASE_URL = db_config["url"]
                logger.info(f"Applied database URL from Nacos")
            if "username" in db_config:
                self.DATABASE_USERNAME = db_config["username"]
            if "password" in db_config:
                self.DATABASE_PASSWORD = db_config["password"]
        
        # 应用Redis配置
        if "redis" in self._nacos_config:
            redis_config = self._nacos_config["redis"]
            if "host" in redis_config:
                self.REDIS_HOST = redis_config["host"]
            if "port" in redis_config:
                self.REDIS_PORT = redis_config["port"]
            if "password" in redis_config:
                self.REDIS_PASSWORD = redis_config["password"]
            if "db" in redis_config:
                self.REDIS_DB = redis_config["db"]
            if "url" in redis_config:
                self.REDIS_URL = redis_config["url"]
                logger.info(f"Applied Redis URL from Nacos")
        
        # 应用服务器配置
        if "server" in self._nacos_config:
            server_config = self._nacos_config["server"]
            if "host" in server_config:
                self.SERVER_HOST = server_config["host"]
            if "port" in server_config:
                self.SERVER_PORT = server_config["port"]
            if "debug" in server_config:
                self.DEBUG = server_config["debug"]
        
        # 应用日志配置
        if "logging" in self._nacos_config:
            logging_config = self._nacos_config["logging"]
            if "level" in logging_config:
                self.LOG_LEVEL = logging_config["level"]
            if "path" in logging_config:
                self.LOG_PATH = logging_config["path"]
            if "error_path" in logging_config:
                self.LOG_PATH_ERROR = logging_config["error_path"]
        
        # 存储第三方服务配置
        if "third_party" in self._nacos_config:
            third_party_config = self._nacos_config["third_party"]
            if "tencent_asr" in third_party_config:
                # 设置腾讯ASR配置到环境变量
                tencent_asr = third_party_config["tencent_asr"]
                if "secret_id" in tencent_asr:
                    os.environ["TENCENT_ASR_SECRET_ID"] = tencent_asr["secret_id"]
                if "secret_key" in tencent_asr:
                    os.environ["TENCENT_ASR_SECRET_KEY"] = tencent_asr["secret_key"]
                logger.info("Applied Tencent ASR configuration from Nacos")
            
            if "sparta_job" in third_party_config:
                # 设置Sparta作业配置到环境变量
                sparta_job = third_party_config["sparta_job"]
                if "address" in sparta_job:
                    os.environ["SPARTA_JOB_ADDRESS"] = sparta_job["address"]
                if "token" in sparta_job:
                    os.environ["SPARTA_JOB_TOKEN"] = sparta_job["token"]
                logger.info("Applied Sparta job configuration from Nacos")
        
        logger.info("Nacos configuration applied successfully")
    
    def get_nacos_config(self, key: str, default: Any = None) -> Any:
        """获取Nacos配置值"""
        return self._nacos_config.get(key, default)
    
    def get_tencent_asr_config(self) -> Dict[str, str]:
        """获取腾讯ASR配置"""
        third_party = self._nacos_config.get("third_party", {})
        return third_party.get("tencent_asr", {})
    
    def get_sparta_job_config(self) -> Dict[str, str]:
        """获取Sparta作业配置"""
        third_party = self._nacos_config.get("third_party", {})
        return third_party.get("sparta_job", {})
    
    def get_kafka_config(self) -> Dict[str, Any]:
        """获取Kafka配置"""
        return self._nacos_config.get("kafka", {})
    
    async def watch_nacos_config(self):
        """监听Nacos配置变更"""
        if not self._nacos_manager or not self._nacos_manager.is_initialized():
            return
        
        async def on_config_change(config_data: str):
            """配置变更回调"""
            logger.info("Nacos configuration changed, reloading...")
            try:
                # 重新加载配置
                self._nacos_config = await self._nacos_manager.load_all_configs(self.ENV)
                await self._apply_nacos_config()
                logger.info("Nacos configuration reloaded successfully")
            except Exception as e:
                logger.error(f"Error reloading Nacos configuration: {e}")
        
        # 监听所有配置
        await self._nacos_manager.watch_all_configs(self.ENV, on_config_change)
    
    async def close_nacos(self):
        """关闭Nacos连接"""
        if self._nacos_manager:
            await self._nacos_manager.close()


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


async def initialize_nacos_config():
    """初始化Nacos配置"""
    settings = get_settings()
    await settings.initialize_nacos()
    await settings.watch_nacos_config()


async def cleanup_nacos_config():
    """清理Nacos配置"""
    settings = get_settings()
    await settings.close_nacos()
