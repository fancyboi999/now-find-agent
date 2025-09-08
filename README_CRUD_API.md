# 🔧 CRUD API 系统文档

## 📋 概述

本文档介绍NOW Find Agent项目中为**Agent**、**LLM**、**Tool**三个核心表实现的完整异步CRUD操作系统。

### 🏗️ 系统架构

基于**四层分离架构**设计：

```
┌─────────────────────────────────────────────────┐
│                API 层 (FastAPI)                  │
│   /api/v1/agents, /api/v1/llms, /api/v1/tools   │
├─────────────────────────────────────────────────┤
│              Service 层 (业务逻辑)                │
│       AgentService, LLMService, ToolService      │
├─────────────────────────────────────────────────┤
│               DAO 层 (数据访问)                   │
│         AgentDao, LLMDao, ToolDao                │
├─────────────────────────────────────────────────┤
│             Model 层 (SQLAlchemy)                │
│          Agent, LLM, Tool (+ BaseModels)         │
└─────────────────────────────────────────────────┘
```

### ⚡ 核心特性

- **异步优先**: 所有操作都基于SQLAlchemy异步引擎
- **类型安全**: 完整的Pydantic schema类型验证
- **统一响应**: 标准化的API响应格式
- **错误处理**: 完善的异常处理和HTTP状态码
- **业务逻辑**: 内置唯一性检查、关联验证等
- **可扩展性**: 基于Base类的可复用架构

## 📊 核心表结构

### 1. Agent（智能代理）

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | Integer | ✅ | 主键ID |
| name | String(256) | ✅ | Agent名称（唯一） |
| description | String(256) | ✅ | Agent描述 |
| status | Integer | ✅ | Agent状态 |
| prompt | String(1024) | ✅ | Agent提示词 |
| bind_tools_list | String(256) | ✅ | 绑定的工具列表 |
| agent_model_id | Integer | ✅ | 使用的LLM模型ID |
| zh_name | String(256) | ❌ | Agent中文名称 |
| is_optional | Boolean | ✅ | 是否可选（默认false） |
| level | Integer | ✅ | Agent级别 |
| created_at | DateTime | ✅ | 创建时间 |
| updated_at | DateTime | ✅ | 更新时间 |
| remark | String(256) | ❌ | 备注 |

### 2. LLM（大语言模型）

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | Integer | ✅ | 主键ID |
| provider | String(256) | ✅ | LLM提供商 |
| model_name | String(256) | ✅ | LLM模型名称（唯一） |
| model_type | String(256) | ✅ | 模型类型（1:basic, 2:思考, 3:多模态） |
| api_key | String(256) | ✅ | API密钥 |
| api_url | String(256) | ✅ | API地址 |
| status | Integer | ✅ | LLM状态 |
| created_at | DateTime | ✅ | 创建时间 |
| updated_at | DateTime | ✅ | 更新时间 |
| remark | String(256) | ❌ | 备注 |

### 3. Tool（工具）

| 字段名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | Integer | ✅ | 主键ID |
| name | String(256) | ✅ | 工具名称（唯一） |
| description | String(256) | ✅ | 工具描述 |
| tool_function | String(256) | ✅ | 工具函数名（唯一） |
| is_direct_return | Boolean | ✅ | 是否直接返回（默认false） |
| status | Integer | ✅ | 工具状态 |
| created_at | DateTime | ✅ | 创建时间 |
| updated_at | DateTime | ✅ | 更新时间 |
| remark | String(256) | ❌ | 备注 |

## 🚀 API 接口说明

### 基础URL格式

```
http://localhost:8000/api/v1/{resource}
```

其中 `{resource}` 为：`agents`、`llms`、`tools`

### 统一响应格式

```json
{
  "code": 200,
  "message": "success",
  "success": true,
  "data": { ... }  // 或 [...] 对于列表
}
```

### Agent API

#### 🟢 创建Agent
```http
POST /api/v1/agents/
Content-Type: application/json

{
  "name": "data_analyst_agent",
  "description": "数据分析专家，帮助用户分析和解释数据",
  "status": 1,
  "prompt": "你是一个专业的数据分析师，能够帮助用户分析各种数据并提供洞察",
  "bind_tools_list": "chart_tool,excel_tool",
  "agent_model_id": 1,
  "zh_name": "数据分析专家",
  "is_optional": false,
  "level": 3,
  "remark": "适用于数据分析场景"
}
```

#### 🔵 获取Agent
```http
GET /api/v1/agents/{agent_id}
GET /api/v1/agents/name/{agent_name}
GET /api/v1/agents/                    # 列表，支持过滤参数
GET /api/v1/agents/active              # 获取激活状态的Agent
```

**列表查询参数：**
- `status`: 过滤状态
- `level`: 过滤级别
- `agent_model_id`: 过滤模型ID
- `keyword`: 关键词搜索（名称、描述、中文名称）
- `is_optional`: 是否可选

#### 🟡 更新Agent
```http
PUT /api/v1/agents/{agent_id}
Content-Type: application/json

{
  "description": "更新后的描述",
  "remark": "更新备注"
}

# 或单独更新状态
PATCH /api/v1/agents/{agent_id}/status?new_status=1
```

#### 🔴 删除Agent
```http
DELETE /api/v1/agents/{agent_id}
```

### LLM API

#### 🟢 创建LLM
```http
POST /api/v1/llms/
Content-Type: application/json

{
  "provider": "openai",
  "model_name": "gpt-4",
  "model_type": "1",
  "api_key": "sk-xxx...",
  "api_url": "https://api.openai.com/v1/chat/completions",
  "status": 1,
  "remark": "GPT-4 模型配置"
}
```

#### 🔵 获取LLM
```http
GET /api/v1/llms/{llm_id}
GET /api/v1/llms/model-name/{model_name}
GET /api/v1/llms/provider/{provider}      # 按提供商
GET /api/v1/llms/type/{model_type}        # 按类型
GET /api/v1/llms/active                   # 激活状态
GET /api/v1/llms/                         # 列表，支持过滤
```

**列表查询参数：**
- `provider`: 过滤提供商
- `model_type`: 过滤模型类型
- `status`: 过滤状态
- `keyword`: 关键词搜索（提供商、模型名称）

#### 🟡 更新LLM
```http
PUT /api/v1/llms/{llm_id}
PATCH /api/v1/llms/{llm_id}/status?new_status=1
```

#### 🔴 删除LLM
```http
DELETE /api/v1/llms/{llm_id}
```

#### 🧪 测试LLM连接
```http
POST /api/v1/llms/{llm_id}/test
```

### Tool API

#### 🟢 创建Tool
```http
POST /api/v1/tools/
Content-Type: application/json

{
  "name": "web_search",
  "description": "网络搜索工具，可以搜索互联网信息",
  "tool_function": "web_search_function",
  "is_direct_return": false,
  "status": 1,
  "remark": "基于搜索引擎的网络搜索工具"
}
```

#### 🔵 获取Tool
```http
GET /api/v1/tools/{tool_id}
GET /api/v1/tools/name/{tool_name}
GET /api/v1/tools/function/{tool_function}
GET /api/v1/tools/active                    # 激活状态
GET /api/v1/tools/direct-return?is_direct=true  # 按返回类型
GET /api/v1/tools/                          # 列表，支持过滤
```

**列表查询参数：**
- `status`: 过滤状态
- `is_direct_return`: 是否直接返回
- `keyword`: 关键词搜索（名称、描述、工具函数）

#### 🟡 更新Tool
```http
PUT /api/v1/tools/{tool_id}
PATCH /api/v1/tools/{tool_id}/status?new_status=1
```

#### 🔴 删除Tool
```http
DELETE /api/v1/tools/{tool_id}
```

#### 🧪 验证Tool配置
```http
POST /api/v1/tools/{tool_id}/validate
```

#### 📦 批量操作
```http
POST /api/v1/tools/batch/names
Content-Type: application/json

["tool1", "tool2", "tool3"]
```

## 🧪 测试指南

### 1. 启动应用

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动应用（确保表结构已初始化）
python main.py
```

### 2. 验证表结构

```bash
# 检查表结构是否正确初始化
./tests/check_tables.sh
```

### 3. 运行API测试

```bash
# 运行完整的CRUD API测试
python tests/test_crud_api.py
```

### 4. 手动API测试

```bash
# 使用curl测试
curl -X GET "http://localhost:8000/api/v1/llms/" \
  -H "accept: application/json"

# 创建LLM
curl -X POST "http://localhost:8000/api/v1/llms/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "model_name": "gpt-4",
    "model_type": "1",
    "api_key": "sk-test",
    "api_url": "https://api.openai.com/v1/chat/completions",
    "status": 1
  }'
```

### 5. Swagger UI 测试

访问 `http://localhost:8000/docs` 进行可视化API测试

## 📁 项目文件结构

```
app/
├── dependencies.py           # FastAPI依赖注入
├── schemas/                  # Pydantic数据模型
│   ├── agent.py             # Agent的Schema定义
│   ├── llm.py               # LLM的Schema定义
│   └── tool.py              # Tool的Schema定义
├── orm/
│   ├── dao/                 # 数据访问层
│   │   ├── AgentDao.py      # Agent数据访问对象
│   │   ├── LLMDao.py        # LLM数据访问对象
│   │   └── ToolDao.py       # Tool数据访问对象
│   └── service/             # 业务逻辑层
│       ├── AgentService.py  # Agent业务服务
│       ├── LLMService.py    # LLM业务服务
│       └── ToolService.py   # Tool业务服务
├── api/                     # API路由层
│   ├── agents.py            # Agent API路由
│   ├── llms.py              # LLM API路由
│   └── tools.py             # Tool API路由
└── models/                  # SQLAlchemy模型
    ├── Agent.py             # Agent数据模型
    ├── LLM.py               # LLM数据模型
    └── Tool.py              # Tool数据模型

tests/
├── test_crud_api.py         # CRUD API自动化测试
└── check_tables.sh          # 表结构验证脚本
```

## 🔧 使用示例

### Python客户端示例

```python
import httpx
import asyncio

async def example_usage():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # 1. 创建LLM
        llm_data = {
            "provider": "openai",
            "model_name": "gpt-4",
            "model_type": "1",
            "api_key": "sk-xxx",
            "api_url": "https://api.openai.com/v1/chat/completions",
            "status": 1
        }
        response = await client.post("/api/v1/llms/", json=llm_data)
        llm = response.json()["data"]
        print(f"创建LLM成功: {llm['id']}")
        
        # 2. 创建Tool
        tool_data = {
            "name": "web_search",
            "description": "网络搜索工具",
            "tool_function": "web_search_function",
            "is_direct_return": False,
            "status": 1
        }
        response = await client.post("/api/v1/tools/", json=tool_data)
        tool = response.json()["data"]
        print(f"创建Tool成功: {tool['id']}")
        
        # 3. 创建Agent
        agent_data = {
            "name": "search_agent",
            "description": "搜索专家代理",
            "status": 1,
            "prompt": "你是一个搜索专家",
            "bind_tools_list": "web_search",
            "agent_model_id": llm["id"],
            "level": 1,
            "is_optional": False
        }
        response = await client.post("/api/v1/agents/", json=agent_data)
        agent = response.json()["data"]
        print(f"创建Agent成功: {agent['id']}")

asyncio.run(example_usage())
```

### JavaScript/TypeScript示例

```typescript
interface LLMCreate {
  provider: string;
  model_name: string;
  model_type: string;
  api_key: string;
  api_url: string;
  status: number;
  remark?: string;
}

async function createLLM(data: LLMCreate) {
  const response = await fetch('http://localhost:8000/api/v1/llms/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const result = await response.json();
  return result.data;
}
```

## 🚨 常见问题

### 1. 唯一性约束错误

**问题**: 创建时出现名称已存在错误
```json
{
  "detail": "Agent 名称 'test_agent' 已存在"
}
```

**解决**: 检查名称唯一性，或使用不同的名称

### 2. 外键约束错误

**问题**: 创建Agent时LLM模型ID不存在
```json
{
  "detail": "LLM ID 999 不存在"
}
```

**解决**: 先创建LLM，再创建Agent

### 3. 数据库连接错误

**问题**: 应用启动时数据库连接失败

**解决**: 
1. 检查数据库服务是否启动
2. 验证 `.env` 中的数据库配置
3. 运行表结构检查：`./tests/check_tables.sh`

### 4. API响应超时

**问题**: 请求响应时间过长

**解决**:
1. 检查数据库连接池配置
2. 优化查询条件
3. 考虑添加索引

## 🔮 扩展建议

### 1. 添加分页支持

```python
# 在schemas/base.py中已提供PaginationModel
# 可以扩展API支持分页查询
@router.get("/", response_model=PaginatedResponseModel[AgentResponse])
async def list_agents_paginated(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    # 实现分页逻辑
    pass
```

### 2. 添加批量操作

```python
@router.post("/batch", response_model=DataResponseModel[List[AgentResponse]])
async def batch_create_agents(
    agents: List[AgentCreate],
    db: AsyncSession = Depends(get_db)
):
    # 实现批量创建
    pass
```

### 3. 添加软删除

```python
# 在BaseModels中添加deleted_at字段
# 实现软删除逻辑
```

### 4. 添加审计日志

```python
# 记录所有CRUD操作的审计日志
# 包含操作人、操作时间、操作类型等
```

## 📈 性能优化

1. **数据库索引**: 为常用查询字段添加索引
2. **连接池**: 优化数据库连接池配置
3. **缓存**: 对频繁查询的数据添加Redis缓存
4. **批量操作**: 支持批量CRUD减少数据库往返
5. **异步优化**: 利用asyncio.gather并发处理无依赖操作

---

✅ **CRUD系统已完成**，提供了完整的、符合异步编程最佳实践的基础CRUD操作！
