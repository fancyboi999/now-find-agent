"""
Nacos连接配置
定义Nacos客户端的连接参数和认证信息
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class NacosSettings(BaseSettings):
    """Nacos连接配置"""
    
    # Nacos服务器配置
    NACOS_SERVER: str = Field(
        default="localhost:8848",
        description="Nacos服务器地址"
    )
    NACOS_NAMESPACE: str = Field(
        default="public",
        description="Nacos命名空间"
    )
    NACOS_GROUP: str = Field(
        default="DEFAULT_GROUP",
        description="Nacos分组"
    )
    
    # Nacos认证配置
    NACOS_ACCESS_KEY: Optional[str] = Field(
        default=None,
        description="Nacos访问密钥"
    )
    NACOS_SECRET_KEY: Optional[str] = Field(
        default=None,
        description="Nacos密钥"
    )
    
    # 配置文件名称
    NACOS_BASE_CONFIG: str = Field(
        default="sparta-now-find-feign-base-config",
        description="基础配置文件名"
    )
    NACOS_DYNAMIC_CONFIG: str = Field(
        default="sparta-now-find-feign-dynamic-config",
        description="动态配置文件名"
    )
    NACOS_COMMON_CONFIG: str = Field(
        default="common-springcloud-config",
        description="公共配置文件名"
    )
    
    # 其他配置
    NACOS_TIMEOUT: int = Field(
        default=30,
        description="Nacos连接超时时间"
    )
    NACOS_MAX_RETRY: int = Field(
        default=3,
        description="Nacos最大重试次数"
    )
    NACOS_ENABLED: bool = Field(
        default=True,
        description="是否启用Nacos配置中心"
    )
    
    class Config:
        env_prefix = "NACOS_"
        case_sensitive = True
    
    def get_server_addresses(self) -> str:
        """获取Nacos服务器地址列表"""
        return self.NACOS_SERVER
    
    def get_base_config_id(self, env: str) -> str:
        """获取基础配置ID"""
        return f"{self.NACOS_BASE_CONFIG}-{env}"
    
    def get_dynamic_config_id(self, env: str) -> str:
        """获取动态配置ID"""
        return f"{self.NACOS_DYNAMIC_CONFIG}-{env}"
    
    def get_common_config_id(self, env: str) -> str:
        """获取公共配置ID"""
        return f"{self.NACOS_COMMON_CONFIG}-{env}"