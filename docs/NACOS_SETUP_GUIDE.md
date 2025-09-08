# NOW Find Agent Nacos配置系统使用指南

## 🎯 概述

NOW Find Agent已完成Nacos配置中心的集成，实现了从Spring Boot YAML配置到Python应用配置的自动映射，支持安全配置管理和多环境部署。

## ✨ 核心功能

### 1. 配置中心集成
- ✅ Nacos配置中心连接和配置加载
- ✅ Spring Boot YAML配置自动映射到Python格式
- ✅ 多环境配置支持（dev/pre/prod）
- ✅ 配置优先级管理：环境变量 > Nacos配置 > 默认配置

### 2. 安全配置管理
- ✅ 敏感信息安全存储和访问
- ✅ 开发环境安全配置加载
- ✅ 配置值掩码和日志保护
- ✅ 环境变量和缓存管理

### 3. 数据库配置
- ✅ MySQL/PostgreSQL/SQLite自动检测和配置
- ✅ 异步数据库连接支持
- ✅ 连接池优化和健康检查
- ✅ 动态配置重载支持

### 4. 第三方服务集成
- ✅ 腾讯ASR服务配置
- ✅ Sparta作业调度配置
- ✅ Kafka消息队列配置
- ✅ Redis缓存配置

## 🚀 快速开始

### 1. 环境准备

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
uv sync
```

### 2. 配置设置

#### 开发环境
```bash
# 设置开发环境
export DEPLOY_ENV=dev

# 启动应用
python main.py
```

#### 预发布环境
```bash
# 设置预发布环境
export DEPLOY_ENV=pre

# 配置Nacos认证（如果需要）
export NACOS_ACCESS_KEY=your_access_key_here
export NACOS_SECRET_KEY=your_secret_key_here

# 启动应用
python main.py
```

#### 生产环境
```bash
# 设置生产环境
export DEPLOY_ENV=prod

# 配置Nacos认证
export NACOS_ACCESS_KEY=your_access_key_here
export NACOS_SECRET_KEY=your_secret_key_here

# 启动应用
python main.py
```

### 3. 配置验证

应用启动时会显示配置摘要：

```
=== 配置摘要 ===
数据库: pc-bp178m3uawx9u46jg.rwlb.rds.aliyuncs.com:3306/now_find
Redis: r-bp1q0je62ba9x8hjr3716.redis.rds.aliyuncs.com:6379/0
腾讯ASR: 已配置
Sparta作业: 已配置
```

## 📋 配置结构

### Nacos配置文件

1. **基础配置**: `sparta-now-find-feign-base-config-{env}.yaml`
2. **动态配置**: `sparta-now-find-feign-dynamic-config-{env}.yaml`
3. **公共配置**: `common-springcloud-config-{env}.yaml`

### Spring Boot YAML示例

```yaml
spring:
  datasource:
    normal:
      driver-class-name: com.mysql.cj.jdbc.Driver
      jdbc-url: jdbc:mysql://host:3306/database
      username: username
      password: password
  redis:
    redisson:
      config: |
        singleServerConfig:
          address: "redis://host:6379"
          password: password
          database: 0

tencent:
  asr:
    secretId: your_secret_id
    secretKey: your_secret_key

sparta:
  job:
    address: https://your-job-server.com
    token: your_token
```

### Python配置映射

Nacos配置会自动映射为Python应用配置：

```python
# 数据库配置
{
    "url": "mysql+aiomysql://username:password@host:3306/database",
    "host": "host",
    "port": 3306,
    "database": "database"
}

# Redis配置
{
    "host": "host",
    "port": 6379,
    "password": "password",
    "db": 0,
    "url": "redis://:password@host:6379/0"
}

# 第三方服务配置
{
    "tencent_asr": {
        "secret_id": "your_secret_id",
        "secret_key": "your_secret_key"
    },
    "sparta_job": {
        "address": "https://your-job-server.com",
        "token": "your_token"
    }
}
```

## 🔧 配置管理

### 获取配置

```python
from config.config import get_settings

# 获取配置实例
settings = get_settings()

# 获取数据库URL
db_url = settings.DATABASE_URL

# 获取Redis配置
redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT

# 获取第三方服务配置
tencent_config = settings.get_tencent_asr_config()
sparta_config = settings.get_sparta_job_config()
```

### 安全配置管理

```python
from config.secure_config import get_secure_config_manager

# 获取安全配置管理器
secure_manager = get_secure_config_manager()

# 获取数据库配置
db_config = secure_manager.get_database_config()

# 构建数据库URL
db_url = secure_manager.build_database_url()

# 获取Redis配置
redis_config = secure_manager.get_redis_config()
```

## 🌍 环境配置

### 开发环境 (dev)
- Nacos服务器: `mse-18f07300-nacos-ans.mse.aliyuncs.com`
- 命名空间: `3f16cc68-f560-42e9-8daf-2ccad2e34b28`
- 分组: `common_group`
- 认证: 无需认证

### 预发布环境 (pre)
- Nacos服务器: `mse-db76bc40-nacos-ans.mse.aliyuncs.com`
- 命名空间: `f53c16dc-a0ae-42df-a64b-f7a84fb011d6`
- 分组: `common_group`
- 认证: 需要AccessKey和SecretKey

### 生产环境 (prod)
- Nacos服务器: `mse-db76bc40-nacos-ans.mse.aliyuncs.com`
- 命名空间: `01191aa2-ab3a-427d-a360-48218a3fb488`
- 分组: `common_group`
- 认证: 需要AccessKey和SecretKey

## 🛡️ 安全特性

### 1. 敏感信息保护
- 敏感配置键自动识别
- 配置值掩码显示
- 安全存储和访问控制

### 2. 环境变量管理
- 敏感信息仅存储在内存中
- 非敏感配置可持久化到环境变量
- 开发环境安全配置加载

### 3. 配置验证
- 配置格式验证
- 连接健康检查
- 配置完整性检查

## 🔍 故障排除

### 1. Nacos连接失败
```
# 检查网络连接
ping your-nacos-server.com

# 检查配置
export NACOS_SERVER=your-nacos-server.com
export NACOS_NAMESPACE=your-namespace
```

### 2. 配置加载失败
```
# 查看详细日志
export LOG_LEVEL=DEBUG

# 检查环境变量
echo $DEPLOY_ENV
echo $USE_NACOS
```

### 3. 数据库连接失败
```
# 检查数据库配置
python -c "from config.config import get_settings; print(get_settings().DATABASE_URL)"

# 测试数据库连接
python -c "from app.providers.database import check_database_health; import asyncio; asyncio.run(check_database_health())"
```

## 📊 监控和日志

### 配置加载日志
```
INFO: Nacos client initialized for namespace: xxx
INFO: Configuration mapping completed
INFO: Configuration initialized successfully
```

### 数据库连接日志
```
INFO: 使用配置的数据库URL: xxx...
INFO: 数据库重新初始化成功: MYSQL
INFO: 数据库健康检查通过
```

### 配置摘要日志
```
=== 配置摘要 ===
数据库: host:port/database
Redis: host:port/db
腾讯ASR: 已配置
Sparta作业: 已配置
```

## 🚀 部署指南

### 1. Docker部署
```dockerfile
ENV DEPLOY_ENV=prod
ENV USE_NACOS=true
ENV NACOS_SERVER=your-nacos-server.com
ENV NACOS_NAMESPACE=your-namespace
ENV NACOS_ACCESS_KEY=your-access-key
ENV NACOS_SECRET_KEY=your-secret-key
```

### 2. Kubernetes部署
```yaml
env:
  - name: DEPLOY_ENV
    value: "prod"
  - name: USE_NACOS
    value: "true"
  - name: NACOS_SERVER
    value: "your-nacos-server.com"
  - name: NACOS_NAMESPACE
    value: "your-namespace"
  - name: NACOS_ACCESS_KEY
    valueFrom:
      secretKeyRef:
        name: nacos-secret
        key: access-key
  - name: NACOS_SECRET_KEY
    valueFrom:
      secretKeyRef:
        name: nacos-secret
        key: secret-key
```

## 📈 后续优化计划

1. **配置热更新**: 完善配置监听和动态更新功能
2. **配置加密**: 实现敏感配置的加密存储
3. **配置版本管理**: 添加配置版本控制和回滚功能
4. **配置验证**: 增强配置格式和有效性验证
5. **性能优化**: 优化配置加载和缓存机制

## 📞 技术支持

如有问题，请查看：
1. 应用日志中的详细错误信息
2. Nacos配置中心的状态
3. 网络连接和认证信息
4. 环境变量配置是否正确

---

🎉 **恭喜！NOW Find Agent现已完成Nacos配置中心集成，支持安全、统一的配置管理！**