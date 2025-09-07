# 🚀 FastAPI Base - 现代化企业级脚手架

一个基于 FastAPI 的现代化、企业级 Python Web API 脚手架，采用最新的项目管理和开发实践，支持多环境、多数据库，开箱即用。

## ✨ 核心特性

- 🚀 **现代化架构** - 基于 FastAPI + Pydantic + SQLAlchemy 的异步优先架构
- 🏗️ **企业级设计** - Provider模式、依赖注入、清晰的分层架构
- 🌍 **多环境支持** - dev/test/uat/prod 四环境架构，智能配置管理
- 🗄️ **多数据库支持** - SQLite/PostgreSQL/MySQL，智能检测与优化
- 📦 **现代包管理** - pyproject.toml + uv，分组依赖管理
- 🛠️ **完整工具链** - 集成开发、测试、部署全套工具
- 📖 **自动文档** - OpenAPI/Swagger 自动生成，开发者友好
- 🔧 **生产就绪** - 考虑性能、安全、监控等生产需求

## 📊 项目结构

```
fastapi-base/
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
│   │   ├── schemas/            # Pydantic 模式
│   │   ├── services/           # 业务服务
│   │   ├── orm/                # ORM相关（DAO/Entity/Service）
│   │   ├── utils/              # 工具函数
│   │   └── exceptions/         # 异常处理
│   ├── config/                 # 配置管理
│   └── bootstrap/              # 应用启动
├── 📖 文档 & 静态文件
│   ├── static/                 # 静态文件
│   └── tests/                  # 测试代码
└── 📝 入口文件
    └── main.py                 # 应用入口
```

## 🚀 3步快速启动

### 第1步：准备环境

```bash
# 安装 uv (推荐的包管理器)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境
uv venv

# 激活环境
source .venv/bin/activate  # macOS/Linux
# 或者 Windows: .venv\Scripts\activate
```

### 第2步：安装依赖

```bash
# 推荐：开发环境完整安装
uv pip install -e ".[dev,database]"

# 或者：基础安装
uv pip install -e .

# 或者：完整功能安装
uv pip install -e ".[all]"
```

### 第3步：启动应用

```bash
# 方式1：直接启动
python main.py

# 方式2：使用make命令（推荐）
make dev

# 方式3：使用环境切换
./switch-env.sh dev
```

## 🎯 成功验证

启动成功后访问：
- 🌐 **应用主页**: http://localhost:8000
- 📖 **API文档**: http://localhost:8000/docs
- 🏥 **健康检查**: http://localhost:8000/health/

看到以下信息说明成功：
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 🔧 常用命令

### 项目管理
```bash
make help          # 📋 查看所有可用命令
make version       # 📌 显示项目版本
make deps          # 📦 显示已安装的依赖
make clean         # 🧹 清理项目临时文件
```

### 开发相关
```bash
make dev           # 🚀 启动开发服务器
make test          # 🧪 运行测试
make format        # ✨ 格式化代码
make lint          # 🔍 代码检查
```

### 环境管理
```bash
make env-dev       # 🔧 切换到开发环境
make env-test      # 🧪 切换到测试环境
make env-uat       # 🎯 切换到UAT环境
make env-prod      # 🚀 切换到生产环境

# 或使用脚本
./switch-env.sh dev    # 开发环境
./switch-env.sh test   # 测试环境
./switch-env.sh uat    # UAT环境
./switch-env.sh prod   # 生产环境
```

## 🌍 多环境配置

### 环境对比

| 环境 | DEPLOY_ENV | 配置文件 | 数据库推荐 | 调试模式 | 工作进程 |
|------|------------|----------|------------|----------|----------|
| **开发** | `dev` | `.env` + `.env.dev` | SQLite | ✅ | 1 |
| **测试** | `test` | `.env` + `.env.test` | SQLite (内存) | ✅ | 1 |
| **UAT** | `uat` | `.env` + `.env.uat` | PostgreSQL/MySQL | ❌ | 2 |
| **生产** | `prod` | `.env` + `.env.prod` | PostgreSQL/MySQL | ❌ | 4 |

### 配置优先级
1. **环境变量** (最高优先级)
2. **环境特定文件** (如 `.env.dev`)
3. **基础配置文件** (`.env`)
4. **代码默认值** (最低优先级)

## 🗄️ 数据库配置

### 支持的数据库

#### SQLite (开发环境推荐)
```bash
DATABASE_URL=sqlite+aiosqlite:///./app.db
```
- ✅ 无需安装数据库服务器，开箱即用
- ✅ 适合开发和测试

#### PostgreSQL (生产环境推荐)
```bash
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name
```
- ✅ 功能强大，优秀的并发性能
- ✅ 适合大型应用

#### MySQL (常用选择)
```bash
DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/database_name
```
- ✅ 广泛使用，生态成熟
- ✅ 云服务支持好

### 快速配置示例

编辑 `.env` 文件：
```bash
# 开发环境 - SQLite
DATABASE_URL=sqlite+aiosqlite:///./app.db

# 生产环境 - PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:pass@server:5432/mydb

# 生产环境 - MySQL  
DATABASE_URL=mysql+aiomysql://user:pass@server:3306/mydb
```

## 📦 依赖管理

### 核心依赖 (自动安装)
- `fastapi` - Web框架
- `uvicorn[standard]` - ASGI服务器  
- `pydantic` - 数据验证
- `sqlalchemy[asyncio]` - ORM
- `redis` - 缓存
- `loguru` - 日志

### 可选依赖组
```bash
# 数据库驱动
uv pip install -e ".[database]"

# AI/LLM 功能
uv pip install -e ".[ai]"

# 开发工具
uv pip install -e ".[dev]"

# 生产部署
uv pip install -e ".[production]"

# 完整安装
uv pip install -e ".[all]"
```

## 🏗️ 开发指南

### 添加新的 API 接口

1. **定义 Pydantic 模型**
```python
# app/schemas/user.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
```

2. **创建路由文件**
```python
# app/api/users.py
from fastapi import APIRouter
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    return {"id": 1, "name": user.name, "email": user.email}
```

3. **注册路由**
```python
# main.py
from app.api.users import router as users_router
app.include_router(users_router)
```

### 数据库操作

```python
# app/orm/entity/user.py
from app.orm.entity.BaseEntity import BaseEntity
from sqlalchemy import Column, String

class User(BaseEntity):
    __tablename__ = "users"
    
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

# app/orm/dao/user_dao.py
from app.orm.dao.BaseDao import BaseDao
from app.orm.entity.user import User

class UserDao(BaseDao[User]):
    def __init__(self):
        super().__init__(User)
```

### Provider 架构

添加新的服务提供者：
```python
# app/providers/new_provider.py
from fastapi import FastAPI
from config.config import Settings

async def register(app: FastAPI, settings: Settings):
    """注册新服务"""
    # 初始化逻辑
    pass

# 在 bootstrap/application.py 中注册
from app.providers import new_provider
await new_provider.register(app, settings)
```

## 🚨 常见问题

### Python 版本问题
```bash
# 错误：requires-python = ">=3.11"
# 解决：升级 Python 到 3.11+
pyenv install 3.11.9
pyenv global 3.11.9
```

### uv 命令找不到
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # 或重新打开终端
```

### 依赖安装失败
```bash
# 清理重装
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev,database]"
```

### 应用启动失败
```bash
# 检查配置
cat .env

# 检查导入
python -c "from app.providers import app_provider; print('OK')"

# 查看详细错误
python main.py
```

## 🚀 部署指南

### Docker 部署
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv pip install -e ".[production]"

EXPOSE 8000
CMD ["python", "main.py"]
```

### 生产环境配置
```bash
export DEPLOY_ENV=prod
export DEBUG=false
export DATABASE_URL=postgresql://user:pass@db:5432/prod
export REDIS_URL=redis://redis:6379
```

## 💡 开发流程建议

### 日常开发
```bash
# 1. 激活环境
source .venv/bin/activate

# 2. 启动开发服务器
make dev

# 3. 开发完成后
make test      # 运行测试
make format    # 格式化代码
make lint      # 代码检查
```

### 新功能开发
```bash
# 1. 创建分支
git checkout -b feature/new-feature

# 2. 开发功能
make dev

# 3. 测试
make test

# 4. 提交
git add .
git commit -m "feat: 添加新功能"
git push origin feature/new-feature
```

## 🎯 最佳实践

1. **分层架构** - 严格遵循 API → Service → DAO 的分层模式
2. **类型提示** - 所有函数都使用完整的类型注解
3. **配置外部化** - 通过环境变量管理不同环境的配置
4. **异步优先** - 所有I/O操作使用异步模式
5. **统一响应** - 使用标准的响应模型格式
6. **异常处理** - 通过全局异常处理器统一错误响应
7. **文档优先** - 所有 API 都包含完整的文档说明

## 🔗 相关链接

- 📖 [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- 🗄️ [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- 📦 [uv 包管理器](https://github.com/astral-sh/uv)
- 🔧 [Pydantic 文档](https://docs.pydantic.dev/)

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 📄 许可证

本项目基于 MIT 许可证发布。详情请查看 [LICENSE](LICENSE) 文件。

---

## 🎉 开始您的开发之旅

现在您已经掌握了 FastAPI Base 的完整使用方法！

- ✅ 快速启动项目
- ✅ 多环境配置管理  
- ✅ 多数据库支持
- ✅ 企业级架构设计
- ✅ 完整的开发工具链

**立即开始构建您的下一个伟大项目吧！** 🚀

如有问题或建议，欢迎提交 Issue 或 Pull Request。
