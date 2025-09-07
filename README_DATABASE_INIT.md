# 🗄️ 数据库表结构初始化确认指南

## 📋 概述

NOW Find Agent 使用 SQLAlchemy 的异步自动初始化机制来管理数据库表结构。本指南提供多种方法来确认表结构是否已正确初始化。

## 🎯 核心表结构

当前应用定义了以下核心表：

| 表名 | 模型类 | 描述 |
|------|--------|------|
| `agent` | `Agent` | 智能代理配置表 |
| `llm` | `LLM` | 大语言模型配置表 |
| `tool` | `Tool` | 工具配置表 |

所有表都包含以下公共字段：
- `created_at` - 创建时间
- `updated_at` - 更新时间  
- `remark` - 备注信息

## 🔧 初始化机制

### 触发时机
表结构在应用启动时自动创建，具体在 `app/providers/app_provider.py` 的 FastAPI 生命周期管理中：

```python
# 检查并创建数据库表结构
try:
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )  # 检查数据库中是否存在相应的表, 如不存在则创建
    logger.info("数据库表结构检查完成")
except Exception as e:
    logger.error(f"数据库表结构检查失败: {e}")
```

### 支持的数据库
- **SQLite** (默认) - 开发环境推荐
- **PostgreSQL** - 生产环境推荐
- **MySQL/MariaDB** - 备选方案

## ✅ 确认方法

### 方法一：运行专用验证脚本（推荐）

#### 🐍 Python 验证脚本
```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行详细的表结构验证
python tests/test_database_tables.py
```

**输出示例：**
```
🔍 开始数据库表结构验证...
📊 数据库类型: sqlite
📊 Schema名称: app
✅ 数据库连接正常
📋 数据库中现有表: ['agent', 'llm', 'tool']

🔍 检查表: agent
✅ 表 'agent' 结构检查完成
🎉 数据库表结构验证通过!
```

#### 🚀 Shell 快速检查脚本
```bash
# 一键检查（自动处理环境激活）
./tests/check_tables.sh
```

### 方法二：查看应用启动日志

#### 启动应用并观察日志
```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动应用
python main.py
```

#### 关键日志信息
应该看到以下成功日志：
```
✅ sqlite 数据库健康检查通过
📊 数据库连接池状态: {'size': 0, 'checked_in': 0, 'checked_out': 0, 'overflow': 0}
数据库表结构检查完成
🎉 应用启动完成,开始提供服务
```

**⚠️ 错误日志示例：**
```
❌ 数据库连接健康检查失败
❌ 数据库表结构检查失败: [具体错误信息]
```

### 方法三：直接数据库查询

#### SQLite（默认配置）
```bash
# 查看 SQLite 数据库文件
ls -la app.db

# 使用 SQLite 命令行工具
sqlite3 app.db ".tables"
# 应该显示: agent  llm  tool

# 查看表结构
sqlite3 app.db ".schema agent"
```

#### PostgreSQL
```sql
-- 连接数据库后执行
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('agent', 'llm', 'tool');

-- 查看表结构
\d agent
\d llm  
\d tool
```

#### MySQL
```sql
-- 查看表
SHOW TABLES LIKE 'agent';
SHOW TABLES LIKE 'llm';
SHOW TABLES LIKE 'tool';

-- 查看表结构
DESCRIBE agent;
DESCRIBE llm;
DESCRIBE tool;
```

### 方法四：使用 FastAPI 健康检查端点

```bash
# 启动应用后访问健康检查端点
curl http://localhost:8000/health

# 预期响应
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "database": "connected"
}
```

## 🚨 故障排查

### 常见问题及解决方案

#### 1. 数据库连接失败
**症状：** `数据库连接健康检查失败`

**解决方案：**
- 检查 `.env` 文件中的 `DATABASE_URL` 配置
- 确保数据库服务已启动
- 验证连接参数（主机、端口、用户名、密码）

#### 2. 表结构创建失败
**症状：** `数据库表结构检查失败`

**解决方案：**
- 检查数据库用户权限
- 确保 Schema 存在（PostgreSQL）
- 查看详细错误日志进行诊断

#### 3. 部分表缺失
**症状：** 验证脚本显示某些表不存在

**解决方案：**
- 确保所有模型类都正确导入
- 检查模型类是否继承了 `Base`
- 重新启动应用触发表创建

#### 4. 环境配置问题
**症状：** 应用使用了错误的数据库

**解决方案：**
- 检查 `DEPLOY_ENV` 环境变量设置
- 确认加载了正确的 `.env` 文件
- 查看应用启动日志中的环境信息

## 📚 最佳实践

### 开发环境
1. **使用默认 SQLite** - 无需额外配置，开箱即用
2. **定期运行验证脚本** - 确保表结构一致性
3. **查看启动日志** - 及时发现初始化问题

### 生产环境
1. **使用 PostgreSQL** - 更好的性能和并发支持
2. **配置连接池** - 优化数据库连接管理
3. **监控表结构** - 设置自动化检查
4. **备份策略** - 定期备份数据库结构和数据

### 部署流程
1. **环境检查** - 运行 `./tests/check_tables.sh`
2. **应用启动** - 观察初始化日志
3. **功能验证** - 访问健康检查端点
4. **监控设置** - 配置数据库监控

## 🛠️ 开发工具

### 快速命令
```bash
# 环境准备
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 表结构验证
./tests/check_tables.sh

# 应用启动（开发模式）
python main.py

# 健康检查
curl http://localhost:8000/health
```

### IDE 集成
- **VS Code** - 使用 SQLite 扩展查看数据库
- **PyCharm** - 内置数据库工具查看表结构
- **DBeaver** - 通用数据库管理工具

## 📞 支持

如果遇到问题：
1. 查看应用启动日志
2. 运行验证脚本获取详细信息
3. 检查数据库连接配置
4. 参考本指南的故障排查部分

---

**📝 注意：** 表结构会在每次应用启动时进行检查，如果表不存在会自动创建。这是 SQLAlchemy 的 `create_all()` 方法的预期行为。
