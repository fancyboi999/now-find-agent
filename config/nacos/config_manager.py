"""
Nacos配置管理器
提供配置的加载、监听和动态更新功能
"""

import asyncio
import yaml
from typing import Any, Dict, Optional, Callable, Awaitable
from functools import lru_cache
from loguru import logger

try:
    from nacos import NacosClient
except ImportError:
    logger.warning("Nacos SDK not installed, falling back to local configuration")
    NacosClient = None

from .settings import NacosSettings
from .config_mapper import NacosConfigMapper


class NacosConfigManager:
    """Nacos配置管理器"""
    
    def __init__(self, settings: NacosSettings):
        self.settings = settings
        self.client: Optional[NacosClient] = None
        self.config_cache: Dict[str, Any] = {}
        self.listeners: Dict[str, Callable[[str], Awaitable[None]]] = {}
        self._initialized = False
        
    async def initialize(self) -> bool:
        """初始化Nacos客户端"""
        if not self.settings.NACOS_ENABLED or not NacosClient:
            logger.info("Nacos configuration disabled or SDK not available")
            return False
            
        try:
            # 创建Nacos客户端
            self.client = NacosClient(
                server_addresses=self.settings.get_server_addresses(),
                namespace=self.settings.NACOS_NAMESPACE
            )
            
            # 设置认证信息（如果需要）
            if self.settings.NACOS_ACCESS_KEY and self.settings.NACOS_SECRET_KEY:
                self.client.set_access_key_secret(
                    self.settings.NACOS_ACCESS_KEY,
                    self.settings.NACOS_SECRET_KEY
                )
            
            logger.info(f"Nacos client initialized for namespace: {self.settings.NACOS_NAMESPACE}")
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Nacos client: {e}")
            return False
    
    async def load_config(self, config_id: str, group: str = None) -> Dict[str, Any]:
        """加载配置"""
        if not self._initialized:
            return {}
            
        try:
            group = group or self.settings.NACOS_GROUP
            config_content = self.client.get_config(
                data_id=config_id,
                group=group
            )
            
            if config_content:
                # 解析YAML配置
                config_data = yaml.safe_load(config_content) or {}
                self.config_cache[f"{group}:{config_id}"] = config_data
                
                logger.info(f"Loaded configuration: {group}:{config_id}")
                return config_data
            else:
                logger.warning(f"Empty configuration: {group}:{config_id}")
                return {}
                
        except Exception as e:
            logger.error(f"Failed to load config {config_id}: {e}")
            return {}
    
    async def load_all_configs(self, env: str) -> Dict[str, Any]:
        """加载所有配置"""
        if not self._initialized:
            return {}
            
        spring_configs = {}
        
        # 加载基础配置
        base_config = await self.load_config(
            self.settings.get_base_config_id(env)
        )
        spring_configs.update(base_config)
        
        # 加载动态配置
        dynamic_config = await self.load_config(
            self.settings.get_dynamic_config_id(env)
        )
        spring_configs.update(dynamic_config)
        
        # 加载公共配置
        common_config = await self.load_config(
            self.settings.get_common_config_id(env)
        )
        spring_configs.update(common_config)
        
        # 映射Spring Boot配置为Python应用配置
        configs = NacosConfigMapper.map_all_configs(spring_configs)
        
        logger.info(f"Loaded and mapped all configurations for environment: {env}")
        return configs
    
    async def watch_config(self, config_id: str, callback: Callable[[str], Awaitable[None]], group: str = None) -> bool:
        """监听配置变更"""
        if not self._initialized:
            return False
            
        try:
            group = group or self.settings.NACOS_GROUP
            
            # TODO: Nacos SDK API不兼容，暂时禁用监听功能
            # def config_callback(data):
            #     # 在异步事件循环中执行回调
            #     asyncio.create_task(callback(data))
            # 
            # self.client.add_config_watcher(
            #     data_id=config_id,
            #     group=group,
            #     callback=config_callback
            # )
            
            self.listeners[f"{group}:{config_id}"] = callback
            logger.info(f"Config watcher disabled due to API incompatibility: {group}:{config_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to watch config {config_id}: {e}")
            return False
    
    async def watch_all_configs(self, env: str, callback: Callable[[str], Awaitable[None]]) -> bool:
        """监听所有配置变更"""
        if not self._initialized:
            return False
            
        success = True
        
        # 监听基础配置
        success &= await self.watch_config(
            self.settings.get_base_config_id(env),
            callback
        )
        
        # 监听动态配置
        success &= await self.watch_config(
            self.settings.get_dynamic_config_id(env),
            callback
        )
        
        # 监听公共配置
        success &= await self.watch_config(
            self.settings.get_common_config_id(env),
            callback
        )
        
        return success
    
    def get_cached_config(self, config_id: str, group: str = None) -> Dict[str, Any]:
        """获取缓存的配置"""
        key = f"{group or self.settings.NACOS_GROUP}:{config_id}"
        return self.config_cache.get(key, {})
    
    def is_initialized(self) -> bool:
        """检查是否已初始化"""
        return self._initialized
    
    async def close(self):
        """关闭Nacos客户端"""
        if self.client:
            try:
                # TODO: Nacos SDK API不兼容，暂时禁用监听器清理
                # 清理所有监听器
                # for listener_key in self.listeners:
                #     config_id = listener_key.split(":", 1)[1]
                #     self.client.remove_config_watcher(config_id)
                
                self.listeners.clear()
                self.config_cache.clear()
                logger.info("Nacos client closed")
            except Exception as e:
                logger.error(f"Error closing Nacos client: {e}")


@lru_cache()
def get_nacos_manager() -> NacosConfigManager:
    """获取Nacos配置管理器实例"""
    settings = NacosSettings()
    return NacosConfigManager(settings)