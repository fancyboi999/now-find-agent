# 🌍 多环境配置指南

## 环境架构

```
fastapi-scaffold/
├── .env              # 基础配置，所有环境共享
├── .env.dev          # 开发环境特定配置
├── .env.test         # 测试环境特定配置
├── .env.uat          # UAT环境特定配置
├── .env.prod         # 生产环境特定配置
└── .env.scaffold     # 脚手架模板
```

## 🚀 环境切换

通过设置 `DEPLOY_ENV` 环境变量来切换环境：

```bash
# 开发环境 (默认)
export DEPLOY_ENV=dev
python main.py

# 测试环境
export DEPLOY_ENV=test
python main.py

# UAT环境
export DEPLOY_ENV=uat
python main.py

# 生产环境
export DEPLOY_ENV=prod
python main.py
```

## 📊 环境对比

| 环境 | DEPLOY_ENV | 配置文件 | 数据库推荐 | 调试模式 | 工作进程 |
|------|------------|----------|------------|----------|----------|
| **开发** | `dev` | `.env` + `.env.dev` | SQLite | ✅ | 1 |
| **测试** | `test` | `.env` + `.env.test` | SQLite (内存) | ✅ | 1 |
| **UAT** | `uat` | `.env` + `.env.uat` | PostgreSQL/MySQL | ❌ | 2 |
| **生产** | `prod` | `.env` + `.env.prod` | PostgreSQL/MySQL | ❌ | 4 |

## 🗄️ 数据库配置策略

### 开发环境 (dev)
```bash
# 快速启动，使用SQLite
DATABASE_URL=sqlite+aiosqlite:///./dev_app.db
```

### 测试环境 (test)
```bash
# 使用内存数据库，测试后自动清理
DATABASE_URL=sqlite+aiosqlite:///:memory:
```

### UAT环境 (uat)
```bash
# 使用与生产环境相同类型的数据库
DATABASE_URL=postgresql+asyncpg://uat_user:uat_pass@uat-server:5432/app_uat
# 或
DATABASE_URL=mysql+aiomysql://uat_user:uat_pass@uat-server:3306/app_uat
```

### 生产环境 (prod)
```bash
# 高性能数据库配置
DATABASE_URL=postgresql+asyncpg://prod_user:strong_pass@prod-server:5432/app_prod
# 或
DATABASE_URL=mysql+aiomysql://prod_user:strong_pass@prod-server:3306/app_prod
```

## 🔧 配置优先级

Pydantic会按以下优先级加载配置：

1. **环境变量** (最高优先级)
2. **环境特定文件** (如 `.env.dev`)
3. **基础配置文件** (`.env`)
4. **代码默认值** (最低优先级)

## 📋 快速设置脚本

创建快速环境切换脚本：

```bash
# 创建环境切换脚本
cat > switch-env.sh << 'SCRIPT'
#!/bin/bash
ENV=${1:-dev}
export DEPLOY_ENV=$ENV
echo "🌍 切换到 $ENV 环境"
echo "📁 配置文件: .env + .env.$ENV"
python main.py
SCRIPT

chmod +x switch-env.sh
```

使用方法：
```bash
./switch-env.sh dev   # 开发环境
./switch-env.sh test  # 测试环境
./switch-env.sh uat   # UAT环境
./switch-env.sh prod  # 生产环境
```

## 🔒 安全注意事项

### 1. 敏感信息管理
```bash
# ❌ 不要在配置文件中写明文密码
DATABASE_URL=mysql://user:password123@server/db

# ✅ 使用环境变量
DATABASE_URL=mysql://user:${DB_PASSWORD}@server/db
```

### 2. 文件权限
```bash
# 设置配置文件权限，防止其他用户读取
chmod 600 .env*
```

### 3. 版本控制
```bash
# .gitignore 中添加敏感配置文件
echo ".env.prod" >> .gitignore
echo ".env.uat" >> .gitignore
echo "*.local" >> .gitignore
```

## �� 部署建议

### Docker部署
```dockerfile
# Dockerfile
ENV DEPLOY_ENV=prod
COPY .env .env.prod ./
```

### Kubernetes部署
```yaml
# deployment.yaml
env:
- name: DEPLOY_ENV
  value: "prod"
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: url
```

## 🧪 测试不同环境

```bash
# 测试配置加载
python -c "
from config.config import get_settings
import os

for env in ['dev', 'test', 'uat', 'prod']:
    os.environ['DEPLOY_ENV'] = env
    settings = get_settings()
    print(f'{env}: {settings.__class__.__name__} - Debug: {settings.DEBUG}')
"
```
