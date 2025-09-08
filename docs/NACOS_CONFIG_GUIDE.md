# Nacos配置中心使用指南

## 概述

本项目已集成Nacos配置中心，支持统一配置管理、动态配置更新和多环境配置。

## 功能特性

- ✅ 统一配置管理：通过Nacos配置中心管理所有环境配置
- ✅ 多环境支持：支持dev/pre/prod等多环境配置
- ✅ 配置优先级：环境变量 > Nacos配置 > 默认配置
- ✅ 向后兼容：保持现有配置接口不变
- ✅ 降级支持：Nacos不可用时自动降级到本地配置

## 配置文件结构

### Nacos配置文件
- **基础配置**: `sparta-now-find-feign-base-config-{env}.yaml`
- **动态配置**: `sparta-now-find-feign-dynamic-config-{env}.yaml`
- **公共配置**: `common-springcloud-config-{env}.yaml`

### 本地配置文件
- `.env` - 通用环境变量
- `.env.dev` - 开发环境配置
- `.env.pre` - 预发布环境配置
- `.env.prod` - 生产环境配置

## 环境配置

### 开发环境 (dev)
```yaml
# Nacos配置
NACOS_SERVER=mse-18f07300-nacos-ans.mse.aliyuncs.com
NACOS_NAMESPACE=3f16cc68-f560-42e9-8daf-2ccad2e34b28
NACOS_GROUP=common_group
# 无需认证
```

### 预发布环境 (pre)
```yaml
# Nacos配置
NACOS_SERVER=mse-db76bc40-nacos-ans.mse.aliyuncs.com
NACOS_NAMESPACE=f53c16dc-a0ae-42df-a64b-f7a84fb011d6
NACOS_GROUP=common_group
NACOS_ACCESS_KEY=your_access_key_here
NACOS_SECRET_KEY=your_secret_key_here
```

### 生产环境 (prod)
```yaml
# Nacos配置
NACOS_SERVER=mse-db76bc40-nacos-ans.mse.aliyuncs.com
NACOS_NAMESPACE=01191aa2-ab3a-427d-a360-48218a3fb488
NACOS_GROUP=common_group
NACOS_ACCESS_KEY=your_access_key_here
NACOS_SECRET_KEY=your_secret_key_here
```

## 使用方法

### 1. 启用/禁用Nacos配置
在环境变量中设置：
```bash
USE_NACOS=true  # 启用Nacos配置中心
USE_NACOS=false # 禁用Nacos配置中心，使用本地配置
```

### 2. 获取配置
```python
from config.config import get_settings

# 获取配置实例
settings = get_settings()

# 获取Nacos配置
db_config = settings.get_nacos_config("database", {})
redis_config = settings.get_nacos_config("redis", {})
```

### 3. 环境切换
```bash
# 设置环境变量
export DEPLOY_ENV=dev    # 开发环境
export DEPLOY_ENV=pre    # 预发布环境
export DEPLOY_ENV=prod   # 生产环境
```

## 配置优先级

1. **环境变量** - 最高优先级
2. **Nacos配置** - 次高优先级
3. **默认配置** - 最低优先级

## 配置热更新

当前版本支持配置的动态加载，但配置监听功能由于SDK API兼容性问题暂时禁用。

## 故障排除

### 1. Nacos连接失败
- 检查Nacos服务器地址和端口
- 验证网络连接
- 确认认证信息正确

### 2. 配置加载失败
- 检查命名空间和分组配置
- 确认配置文件存在
- 查看日志错误信息

### 3. 降级到本地配置
当Nacos不可用时，系统会自动降级到本地环境变量配置。

## 安全注意事项

1. **敏感信息保护**：不要在配置文件中硬编码敏感信息
2. **访问控制**：使用Nacos的权限控制功能
3. **密钥轮换**：定期更换AccessKey和SecretKey
4. **网络安全**：确保Nacos服务器在安全网络环境中

## 监控和日志

- 所有配置操作都会记录到日志中
- Nacos连接状态会被监控
- 配置加载失败会有明确的错误提示

## 后续优化计划

1. 完善配置监听和热更新功能
2. 添加配置加密支持
3. 实现配置版本管理
4. 增强配置验证和校验机制