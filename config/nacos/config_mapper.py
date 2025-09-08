"""
Nacos配置映射器
将Spring Boot YAML配置转换为Python应用配置
"""

import yaml
from typing import Dict, Any, Optional
from loguru import logger


class NacosConfigMapper:
    """Nacos配置映射器"""
    
    @staticmethod
    def map_database_config(spring_config: Dict[str, Any]) -> Dict[str, Any]:
        """映射数据库配置"""
        try:
            datasource = spring_config.get("spring", {}).get("datasource", {})
            normal = datasource.get("normal", {})
            
            if not normal:
                logger.warning("No database configuration found in Nacos")
                return {}
            
            # 构建数据库URL
            driver = normal.get("driver-class-name", "")
            jdbc_url = normal.get("jdbc-url", "")
            username = normal.get("username", "")
            password = normal.get("password", "")
            
            # 转换JDBC URL为异步URL
            if "mysql" in driver.lower() and "mysql" in jdbc_url:
                # 提取主机、端口、数据库名
                import re
                pattern = r"jdbc:mysql://([^:]+):(\d+)/([^?]+)"
                match = re.search(pattern, jdbc_url)
                
                if match:
                    host, port, database = match.groups()
                    async_url = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
                    
                    return {
                        "url": async_url,
                        "username": username,
                        "password": password,
                        "host": host,
                        "port": int(port),
                        "database": database
                    }
            
            logger.warning(f"Unsupported database driver: {driver}")
            return {}
            
        except Exception as e:
            logger.error(f"Error mapping database config: {e}")
            return {}
    
    @staticmethod
    def map_redis_config(spring_config: Dict[str, Any]) -> Dict[str, Any]:
        """映射Redis配置"""
        try:
            redis_config = spring_config.get("spring", {}).get("redis", {})
            redisson = redis_config.get("redisson", {})
            config_str = redisson.get("config", "")
            
            if not config_str:
                logger.warning("No Redis configuration found in Nacos")
                return {}
            
            # 解析Redisson YAML配置
            if isinstance(config_str, str):
                redisson_config = yaml.safe_load(config_str)
            else:
                redisson_config = config_str
            
            single_server = redisson_config.get("singleServerConfig", {})
            
            if not single_server:
                logger.warning("No single server Redis configuration found")
                return {}
            
            address = single_server.get("address", "")
            password = single_server.get("password", "")
            database = single_server.get("database", 0)
            
            # 解析Redis地址
            if address.startswith("redis://"):
                address = address[8:]  # 移除 redis:// 前缀
            
            if ":" in address:
                host, port = address.split(":")
            else:
                host = address
                port = 6379
            
            return {
                "host": host,
                "port": int(port),
                "password": password if password else None,
                "db": int(database),
                "url": f"redis://:{password}@{host}:{port}/{database}" if password else f"redis://{host}:{port}/{database}"
            }
            
        except Exception as e:
            logger.error(f"Error mapping Redis config: {e}")
            return {}
    
    @staticmethod
    def map_server_config(spring_config: Dict[str, Any]) -> Dict[str, Any]:
        """映射服务器配置"""
        try:
            server_config = spring_config.get("server", {})
            
            return {
                "host": "0.0.0.0",  # 默认监听所有接口
                "port": 8000,       # 默认端口
                "debug": True,      # 开发环境默认开启调试
                "max_header_size": server_config.get("max-http-header-size", 65535)
            }
            
        except Exception as e:
            logger.error(f"Error mapping server config: {e}")
            return {}
    
    @staticmethod
    def map_logging_config(spring_config: Dict[str, Any]) -> Dict[str, Any]:
        """映射日志配置"""
        try:
            # Spring Boot的日志配置与Python不同，这里提供默认配置
            return {
                "level": "DEBUG",
                "path": "config/settings/storage/logs/fastapi-{{time:YYYY-MM-DD}}.log",
                "error_path": "config/settings/storage/logs/error/fastapi-{{time:YYYY-MM-DD}}.log",
                "rotation": "00:00",
                "retention": "7 days"
            }
            
        except Exception as e:
            logger.error(f"Error mapping logging config: {e}")
            return {}
    
    @staticmethod
    def map_kafka_config(spring_config: Dict[str, Any]) -> Dict[str, Any]:
        """映射Kafka配置"""
        try:
            kafka_config = spring_config.get("spring", {}).get("kafka", {})
            
            return {
                "bootstrap_servers": kafka_config.get("bootstrap-servers", ""),
                "producer": kafka_config.get("producer", {}),
                "consumer": kafka_config.get("consumer", {})
            }
            
        except Exception as e:
            logger.error(f"Error mapping Kafka config: {e}")
            return {}
    
    @staticmethod
    def map_third_party_config(spring_config: Dict[str, Any]) -> Dict[str, Any]:
        """映射第三方服务配置"""
        try:
            config = {}
            
            # 腾讯ASR配置
            tencent_asr = spring_config.get("tencent", {}).get("asr", {})
            if tencent_asr:
                config["tencent_asr"] = {
                    "secret_id": tencent_asr.get("secretId", ""),
                    "secret_key": tencent_asr.get("secretKey", "")
                }
            
            # Sparta作业配置
            sparta_job = spring_config.get("sparta", {}).get("job", {})
            if sparta_job:
                config["sparta_job"] = {
                    "address": sparta_job.get("address", ""),
                    "token": sparta_job.get("token", "")
                }
            
            return config
            
        except Exception as e:
            logger.error(f"Error mapping third party config: {e}")
            return {}
    
    @staticmethod
    def map_all_configs(spring_config: Dict[str, Any]) -> Dict[str, Any]:
        """映射所有配置"""
        logger.info("Mapping all Nacos configurations...")
        
        mapped_config = {
            "database": NacosConfigMapper.map_database_config(spring_config),
            "redis": NacosConfigMapper.map_redis_config(spring_config),
            "server": NacosConfigMapper.map_server_config(spring_config),
            "logging": NacosConfigMapper.map_logging_config(spring_config),
            "kafka": NacosConfigMapper.map_kafka_config(spring_config),
            "third_party": NacosConfigMapper.map_third_party_config(spring_config)
        }
        
        logger.info("Configuration mapping completed")
        return mapped_config