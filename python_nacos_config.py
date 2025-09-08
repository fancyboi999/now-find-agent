"""
Python连接Nacos配置清单
基于项目中now-find-feign模块的配置信息整理
"""

# Python连接Nacos所需的配置参数

# 1. 开发环境配置 (dev)
NACOS_DEV_CONFIG = {
    "server_addr": "mse-18f07300-nacos-ans.mse.aliyuncs.com",
    "namespace": "3f16cc68-f560-42e9-8daf-2ccad2e34b28",
    "group": "common_group",
    "username": None,  # 开发环境没有用户名密码
    "password": None,
    "access_key": None,
    "secret_key": None
}

# 2. 预发布环境配置 (pre)
NACOS_PRE_CONFIG = {
    "server_addr": "mse-db76bc40-nacos-ans.mse.aliyuncs.com",
    "namespace": "f53c16dc-a0ae-42df-a64b-f7a84fb011d6",
    "group": "common_group",
    "username": None,
    "password": None,
    "access_key": "your_access_key_here",
    "secret_key": "your_secret_key_here"
}

# 3. 生产环境配置 (prod)
NACOS_PROD_CONFIG = {
    "server_addr": "mse-db76bc40-nacos-ans.mse.aliyuncs.com",
    "namespace": "01191aa2-ab3a-427d-a360-48218a3fb488",
    "group": "common_group",
    "username": None,
    "password": None,
    "access_key": "your_access_key_here",
    "secret_key": "your_secret_key_here"
}

# 配置文件列表 (基于feign模块的配置)
CONFIG_FILES = {
    "base_config": "sparta-now-find-feign-base-config-{env}.yaml",
    "dynamic_config": "sparta-now-find-feign-dynamic-config-{env}.yaml",
    "common_config": "common-springcloud-config-{env}.yaml"
}

# Python连接Nacos示例代码
def create_nacos_client(env="dev"):
    """
    创建Nacos客户端
    
    Args:
        env: 环境 (dev/pre/prod)
    
    Returns:
        NacosClient实例
    """
    from nacos import NacosClient
    
    # 根据环境选择配置
    if env == "dev":
        config = NACOS_DEV_CONFIG
    elif env == "pre":
        config = NACOS_PRE_CONFIG
    elif env == "prod":
        config = NACOS_PROD_CONFIG
    else:
        raise ValueError(f"不支持的环境: {env}")
    
    # 创建Nacos客户端
    client = NacosClient(
        server_addresses=config["server_addr"],
        namespace=config["namespace"]
    )
    
    # 设置认证信息
    if config["access_key"] and config["secret_key"]:
        client.set_access_key_secret(config["access_key"], config["secret_key"])
    elif config["username"] and config["password"]:
        client.set_username_password(config["username"], config["password"])
    
    return client

# 使用示例
if __name__ == "__main__":
    # 创建开发环境客户端
    client = create_nacos_client("dev")
    
    # 获取配置示例
    try:
        # 获取动态配置
        dynamic_config = client.get_config(
            "sparta-now-find-feign-dynamic-config-dev.yaml",
            "sparta-now-find-feign"
        )
        print("动态配置:", dynamic_config)
        
        # 获取基础配置
        base_config = client.get_config(
            "sparta-now-find-feign-base-config-dev.yaml",
            "sparta-now-find-feign"
        )
        print("基础配置:", base_config)
        
        # 获取公共配置
        common_config = client.get_config(
            "common-springcloud-config-dev.yaml",
            "common_group"
        )
        print("公共配置:", common_config)
        
    except Exception as e:
        print(f"获取配置失败: {e}")
    
    # 关闭连接
    client.remove_all_config_listeners()

# 配置参数说明
"""
配置参数说明:
1. server_addr: Nacos服务器地址
2. namespace: 命名空间ID，用于环境隔离
3. group: 配置分组，用于配置分类
4. access_key/secret_key: 阿里云MSE的访问密钥（预发布和生产环境需要）
5. username/password: 用户名密码认证（当前项目未使用）

注意事项:
1. 开发环境无需认证信息
2. 预发布和生产环境需要使用access_key和secret_key
3. 配置文件需要指定正确的group:
   - 基础配置和动态配置: group为应用名 (sparta-now-find-feign)
   - 公共配置: group为common_group
4. 配置文件格式为YAML
"""