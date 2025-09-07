# FastAPI 脚手架项目

这是一个基于 FastAPI 的底层脚手架项目，提供了完整的项目结构和基础功能，可用于快速启动新的 FastAPI 应用开发。

## 项目特性

- 🚀 基于 FastAPI 的现代 Python Web 框架
- 🏗️ 清晰的分层架构设计（Controller/Service/DAO）
- 📝 完整的 Pydantic 模型定义和验证
- 🗄️ SQLAlchemy ORM 集成
- 📊 分页和排序支持
- 🔧 统一的配置管理
- 📋 结构化日志记录
- 🛡️ 统一异常处理
- 🏥 健康检查接口
- 📚 自动 API 文档生成

## 项目结构

```
now-find-agent/
├── app/                        # 应用核心代码
│   ├── api/                    # API路由定义
│   │   ├── __init__.py
│   │   ├── health.py          # 健康检查接口
│   │   └── example.py         # 示例接口
│   ├── constants/              # 常量定义
│   │   ├── __init__.py
│   │   └── common.py          # 通用常量
│   ├── exceptions/             # 异常定义
│   │   ├── __init__.py
│   │   └── exception.py       # 自定义异常
│   ├── http/                   # HTTP相关
│   │   ├── api/               # API基础类
│   │   └── middleware/        # 中间件
│   ├── models/                 # 业务模型
│   │   ├── __init__.py
│   │   └── BaseModels.py      # 基础模型
│   ├── orm/                    # ORM相关
│   │   ├── dao/               # 数据访问对象
│   │   ├── entity/            # 实体定义
│   │   ├── service/           # 服务实现
│   │   └── tools/             # ORM工具
│   ├── pages/                  # 分页相关
│   │   ├── __init__.py
│   │   ├── PageHelper.py      # 分页助手
│   │   ├── Pager.py           # 分页器
│   │   ├── Paginate.py        # 分页实现
│   │   └── Sorter.py          # 排序器
│   ├── providers/              # 服务提供者
│   │   ├── __init__.py
│   │   ├── app_provider.py    # 应用提供者
│   │   ├── database/          # 数据库提供者
│   │   ├── exception_provider.py # 异常处理提供者
│   │   └── logging_provider.py # 日志提供者
│   ├── schemas/                # Pydantic模型
│   │   ├── __init__.py
│   │   └── base.py            # 基础Schema
│   ├── services/               # 业务服务
│   │   ├── crypto.py          # 加密服务
│   │   ├── redis.py           # Redis服务
│   │   └── llms/              # LLM服务
│   ├── support/                # 支持工具
│   │   ├── __init__.py
│   │   └── asyncio.py         # 异步工具
│   └── utils/                  # 工具类
│       ├── common/            # 通用工具
│       ├── core/              # 核心工具
│       ├── data/              # 数据工具
│       ├── io/                # IO工具
│       └── web/               # Web工具
├── bootstrap/                  # 应用引导
│   ├── __init__.py
│   └── application.py         # 应用创建
├── config/                     # 配置文件
│   ├── __init__.py
│   └── config.py              # 配置定义
├── static/                     # 静态文件
├── tests/                      # 测试文件
└── main.py                     # 应用入口
```

## 快速开始

### 1. 环境准备

```bash
# 安装 uv (推荐的 Python 包管理器)
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple uv

# 创建虚拟环境并安装依赖
uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi numpy pandas icecream pyyaml matplotlib seaborn "uvicorn[standard]" python-dotenv pydantic_settings pyjwt "passlib[bcrypt]"
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# 环境配置
ENV=dev
DEPLOY_ENV=development

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=true

# 数据库配置（可选）
DATABASE_URL=sqlite:///./app.db

# Redis配置（可选）
REDIS_URL=redis://localhost:6379

# JWT配置
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. 启动应用

```bash
# 方式1：直接运行
python main.py

# 方式2：使用 uvicorn
python -m uvicorn main:app --reload

# 方式3：使用 FastAPI CLI
fastapi dev
```

### 4. 访问应用

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health/
- 示例接口：http://localhost:8000/example/

## 开发指南

### 添加新的 API 接口

1. 在 `app/schemas/` 中定义 Pydantic 模型
2. 在 `app/api/` 中创建路由文件
3. 在 `main.py` 中注册路由

示例：

```python
# app/schemas/user.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

# app/api/users.py
from fastapi import APIRouter
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post("/")
async def create_user(user: UserCreate):
    return {"message": "用户创建成功"}

# main.py
from app.api.users import router as users_router
app.include_router(users_router)
```

### 数据库操作

使用 SQLAlchemy ORM：

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

### 配置管理

根据环境加载不同配置：

```python
# config/config.py
class DevelopmentSettings(BaseAppSettings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./dev.db"

class ProductionSettings(BaseAppSettings):
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://user:pass@localhost/prod"
```

## 技术栈

- **Web框架**: FastAPI
- **数据验证**: Pydantic  
- **ORM**: SQLAlchemy
- **配置管理**: Pydantic Settings
- **日志**: Loguru
- **文档**: 自动生成 OpenAPI/Swagger
- **包管理**: uv

## 最佳实践

1. **分层架构**: 严格遵循 API → Service → DAO 的分层模式
2. **类型提示**: 所有函数都使用完整的类型注解
3. **配置外部化**: 通过环境变量管理不同环境的配置
4. **统一响应**: 使用标准的响应模型格式
5. **异常处理**: 通过全局异常处理器统一错误响应
6. **文档优先**: 所有 API 都包含完整的文档说明

## 部署

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv && uv pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"]
```

### 生产环境配置

```bash
export DEPLOY_ENV=production
export DEBUG=false
export DATABASE_URL=postgresql://user:pass@db:5432/prod
export REDIS_URL=redis://redis:6379
```

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 许可证

MIT License
