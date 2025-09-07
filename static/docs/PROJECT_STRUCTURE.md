# 📁 FastAPI Scaffold 项目结构

## 🏗️ 项目概览

FastAPI Scaffold 是一个现代化、企业级的 Python Web API 脚手架，采用最新的项目管理和开发实践。

```
fastapi-scaffold/
├── 📋 项目配置
│   ├── pyproject.toml          # 现代化项目配置（PEP 518）
│   ├── .env.example            # 环境配置示例
│   ├── .gitignore              # Git 忽略文件
│   ├── Makefile                # 项目管理命令
│   └── setup.sh                # 自动化安装脚本
├── 🌍 环境配置
│   ├── .env                    # 基础环境配置
│   ├── .env.dev                # 开发环境配置
│   ├── .env.test               # 测试环境配置
│   ├── .env.uat                # UAT环境配置
│   ├── .env.prod               # 生产环境配置
│   └── switch-env.sh           # 环境切换工具
├── 🏛️ 应用架构
│   ├── app/                    # 应用核心代码
│   │   ├── api/                # API 路由
│   │   ├── models/             # 数据模型
│   │   ├── providers/          # 服务提供者
│   │   │   ├── app_provider.py    # 应用提供者
│   │   │   ├── database/          # 数据库提供者
│   │   │   ├── exception_provider.py # 异常处理
│   │   │   └── logging_provider.py   # 日志提供者
│   │   ├── schemas/            # Pydantic 模式
│   │   ├── services/           # 业务服务
│   │   └── utils/              # 工具函数
│   ├── config/                 # 配置管理
│   │   └── config.py           # 多环境配置
│   └── bootstrap/              # 应用启动
│       └── application.py      # 应用工厂
├── 📖 文档
│   ├── README.md               # 项目说明
│   ├── database-examples.md    # 数据库配置示例
│   ├── multi-environment-guide.md # 多环境指南
│   └── PROJECT_STRUCTURE.md   # 项目结构说明
├── 🧪 测试
│   └── tests/                  # 测试代码
└── 📝 其他
    ├── main.py                 # 应用入口
    └── requirements.txt        # 传统依赖文件（可选）
```

## 🔧 核心特性

### 1. 现代化项目管理
- ✅ **pyproject.toml** - 符合 PEP 518 标准的项目配置
- ✅ **uv** - 快速的 Python 包管理器
- ✅ **分组依赖** - 按功能组织依赖（dev、database、ai等）
- ✅ **开发工具集成** - Black、isort、pytest、mypy 等

### 2. 多环境支持
- ✅ **四环境架构** - dev、test、uat、prod
- ✅ **环境隔离** - 每个环境独立配置
- ✅ **智能切换** - 一键环境切换工具
- ✅ **配置管理** - Pydantic Settings 驱动

### 3. 多数据库支持
- ✅ **三大数据库** - SQLite、PostgreSQL、MySQL
- ✅ **智能检测** - 自动识别数据库类型
- ✅ **异步优先** - 所有数据库操作异步化
- ✅ **连接优化** - 针对不同数据库优化连接参数

### 4. 企业级架构
- ✅ **Provider 模式** - 模块化服务提供者
- ✅ **依赖注入** - 清晰的依赖管理
- ✅ **异步架构** - 全面的异步支持
- ✅ **可扩展设计** - 易于添加新功能

## 📦 依赖管理

### 核心依赖 (必需)
```toml
[project.dependencies]
fastapi>=0.110.0          # Web 框架
uvicorn[standard]>=0.25.0 # ASGI 服务器
pydantic>=2.5.0           # 数据验证
sqlalchemy[asyncio]>=2.0.0 # ORM
redis>=5.0.0              # 缓存
loguru>=0.7.0             # 日志
```

### 可选依赖组
```bash
# 数据库驱动
pip install fastapi-scaffold[database]

# AI/LLM 功能
pip install fastapi-scaffold[ai]

# 开发工具
pip install fastapi-scaffold[dev]

# 生产部署
pip install fastapi-scaffold[production]

# 完整安装
pip install fastapi-scaffold[all]
```

## 🛠️ 开发工具

### 项目管理命令
```bash
make help          # 查看所有命令
make install-dev   # 安装开发依赖
make dev           # 启动开发服务器
make test          # 运行测试
make format        # 格式化代码
make lint          # 代码检查
```

### 环境切换
```bash
./switch-env.sh dev    # 开发环境
./switch-env.sh test   # 测试环境
./switch-env.sh uat    # UAT环境
./switch-env.sh prod   # 生产环境
```

### 快速初始化
```bash
./setup.sh         # 交互式项目设置
make init          # 快速初始化
```

## 🏗️ Provider 架构

### 命名规范
- ✅ **统一命名** - 所有 provider 使用 `xxx_provider.py` 格式
- ✅ **清晰导入** - 简化的导入路径
- ✅ **功能分离** - 每个 provider 职责单一

### Provider 列表
| Provider | 功能 | 文件路径 |
|----------|------|----------|
| app_provider | 应用生命周期管理 | `app/providers/app_provider.py` |
| database | 数据库连接管理 | `app/providers/database/__init__.py` |
| exception_provider | 异常处理 | `app/providers/exception_provider.py` |
| logging_provider | 日志配置 | `app/providers/logging_provider.py` |

## 🌍 环境配置

### 配置优先级
1. **环境变量** (最高)
2. **环境特定文件** (如 `.env.dev`)
3. **基础配置文件** (`.env`)
4. **代码默认值** (最低)

### 环境特点
| 环境 | 用途 | 数据库推荐 | 调试模式 |
|------|------|------------|----------|
| dev | 日常开发 | SQLite/MySQL | ✅ |
| test | 自动化测试 | SQLite (内存) | ✅ |
| uat | 用户验收测试 | PostgreSQL/MySQL | ❌ |
| prod | 生产环境 | PostgreSQL | ❌ |

## 🔄 版本控制

### 忽略文件
- ✅ **敏感配置** - 生产环境配置文件
- ✅ **临时文件** - 缓存、日志、数据库文件
- ✅ **开发工具** - IDE 配置、编译产物

### 安全实践
- ✅ **配置分离** - 敏感信息不入库
- ✅ **环境隔离** - 各环境独立配置
- ✅ **密钥管理** - 使用环境变量或密钥服务

## �� 部署建议

### 开发环境
```bash
git clone <repository>
./setup.sh
make dev
```

### 生产环境
```bash
export DEPLOY_ENV=prod
make install
make prod-env
```

### Docker 部署
```bash
make docker-build
make docker-run
```

## 📈 扩展指南

### 添加新 Provider
1. 创建 `app/providers/new_provider.py`
2. 实现 `register(app, settings)` 函数
3. 在 `bootstrap/application.py` 中注册

### 添加新环境
1. 创建 `.env.new_env` 配置文件
2. 在 `config/config.py` 中添加环境类
3. 更新 `get_settings()` 函数

### 添加新数据库
1. 安装对应的异步驱动
2. 在 `database/__init__.py` 中添加检测逻辑
3. 配置连接参数和健康检查

---

## 🎯 设计原则

1. **约定优于配置** - 提供合理的默认值
2. **渐进式增强** - 功能模块化，按需加载
3. **开发者友好** - 简化常用操作，提供丰富工具
4. **生产就绪** - 考虑性能、安全、监控等生产需求
5. **现代化标准** - 采用最新的 Python 生态实践

这个脚手架为您提供了一个solid的基础，可以快速开始您的 FastAPI 项目开发！🚀
