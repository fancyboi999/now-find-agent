"""
安全配置管理
处理敏感配置信息的安全存储和访问
"""

import os
from typing import Dict, Optional, Any
from functools import lru_cache
from loguru import logger


class SecureConfigManager:
    """安全配置管理器"""
    
    # 敏感配置键列表
    SENSITIVE_KEYS = [
        "DATABASE_PASSWORD",
        "REDIS_PASSWORD", 
        "NACOS_ACCESS_KEY",
        "NACOS_SECRET_KEY",
        "SECRET_KEY",
        "TENCENT_ASR_SECRET_ID",
        "TENCENT_ASR_SECRET_KEY",
        "SPARTA_JOB_TOKEN",
        "FIRECRAWL_KEY"
    ]
    
    def __init__(self):
        self._config_cache: Dict[str, Any] = {}
    
    def get_secure_config(self, key: str, default: Any = None) -> Any:
        """安全获取配置值"""
        # 1. 优先从环境变量获取
        env_value = os.getenv(key)
        if env_value is not None:
            return env_value
        
        # 2. 从配置缓存获取
        return self._config_cache.get(key, default)
    
    def set_secure_config(self, key: str, value: Any, persistent: bool = False):
        """安全设置配置值"""
        self._config_cache[key] = value
        
        if persistent:
            # 敏感信息不应该持久化到环境变量
            if key in self.SENSITIVE_KEYS:
                logger.warning(f"Sensitive key {key} should not be persisted to environment variables")
            else:
                os.environ[key] = str(value)
    
    def mask_sensitive_value(self, key: str, value: str) -> str:
        """掩码敏感值"""
        if key in self.SENSITIVE_KEYS and value:
            if len(value) <= 8:
                return "*" * len(value)
            else:
                return value[:4] + "*" * (len(value) - 8) + value[-4:]
        return value
    
    def get_database_config(self) -> Dict[str, str]:
        """获取数据库配置"""
        return {
            "username": self.get_secure_config("DATABASE_USERNAME", "nc_test"),
            "password": self.get_secure_config("DATABASE_PASSWORD", "nc_test_2019"),
            "host": self.get_secure_config("DATABASE_HOST", "pc-bp178m3uawx9u46jg.rwlb.rds.aliyuncs.com"),
            "port": int(self.get_secure_config("DATABASE_PORT", "3306")),
            "database": self.get_secure_config("DATABASE_NAME", "now_find")
        }
    
    def get_redis_config(self) -> Dict[str, Any]:
        """获取Redis配置"""
        return {
            "host": self.get_secure_config("REDIS_HOST", "r-bp1q0je62ba9x8hjr3716.redis.rds.aliyuncs.com"),
            "port": int(self.get_secure_config("REDIS_PORT", "6379")),
            "password": self.get_secure_config("REDIS_PASSWORD", "aUP8FM3jFUaYAYz"),
            "db": int(self.get_secure_config("REDIS_DB", "0"))
        }
    
    def get_tencent_asr_config(self) -> Dict[str, str]:
        """获取腾讯ASR配置"""
        return {
            "secret_id": self.get_secure_config("TENCENT_ASR_SECRET_ID", ""),
            "secret_key": self.get_secure_config("TENCENT_ASR_SECRET_KEY", "")
        }
    
    def get_sparta_job_config(self) -> Dict[str, str]:
        """获取Sparta作业配置"""
        return {
            "address": self.get_secure_config("SPARTA_JOB_ADDRESS", ""),
            "token": self.get_secure_config("SPARTA_JOB_TOKEN", "")
        }
    
    def build_database_url(self, config: Dict[str, str] = None) -> str:
        """构建数据库URL"""
        if config is None:
            config = self.get_database_config()
        
        username = config["username"]
        password = config["password"]
        host = config["host"]
        port = config["port"]
        database = config["database"]
        
        return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
    
    def build_redis_url(self, config: Dict[str, Any] = None) -> str:
        """构建Redis URL"""
        if config is None:
            config = self.get_redis_config()
        
        host = config["host"]
        port = config["port"]
        password = config["password"]
        db = config["db"]
        
        if password:
            return f"redis://:{password}@{host}:{port}/{db}"
        else:
            return f"redis://{host}:{port}/{db}"
    
    def load_development_config(self):
        """加载开发环境配置（仅用于开发）"""
        if os.getenv("DEPLOY_ENV") != "dev":
            logger.warning("Development config should only be loaded in dev environment")
            return
        
        # 开发环境配置
        dev_config = {
            "DATABASE_USERNAME": "nc_test",
            "DATABASE_PASSWORD": "nc_test_2019", 
            "DATABASE_HOST": "pc-bp178m3uawx9u46jg.rwlb.rds.aliyuncs.com",
            "DATABASE_PORT": "3306",
            "DATABASE_NAME": "now_find",
            "REDIS_HOST": "r-bp1q0je62ba9x8hjr3716.redis.rds.aliyuncs.com",
            "REDIS_PORT": "6379",
            "REDIS_PASSWORD": "aUP8FM3jFUaYAYz",
            "REDIS_DB": "0",
            "TENCENT_ASR_SECRET_ID": "your_tencent_secret_id_here",
            "TENCENT_ASR_SECRET_KEY": "your_tencent_secret_key_here",
            "SPARTA_JOB_ADDRESS": "https://xxljob-dev.nowcoder.com/sparta-job",
            "SPARTA_JOB_TOKEN": "default_token"
        }
        
        # 只设置非敏感配置到环境变量
        for key, value in dev_config.items():
            if key not in self.SENSITIVE_KEYS:
                os.environ[key] = value
            self._config_cache[key] = value
        
        logger.info("Development configuration loaded securely")
    
    def log_config_summary(self):
        """记录配置摘要（不包含敏感信息）"""
        db_config = self.get_database_config()
        redis_config = self.get_redis_config()
        
        logger.info("=== 配置摘要 ===")
        logger.info(f"数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")
        logger.info(f"Redis: {redis_config['host']}:{redis_config['port']}/{redis_config['db']}")
        logger.info(f"腾讯ASR: {'已配置' if self.get_tencent_asr_config()['secret_id'] else '未配置'}")
        logger.info(f"Sparta作业: {'已配置' if self.get_sparta_job_config()['address'] else '未配置'}")


@lru_cache()
def get_secure_config_manager() -> SecureConfigManager:
    """获取安全配置管理器实例"""
    return SecureConfigManager()