# 📦 多数据库配置示例

FastAPI脚手架支持多种数据库类型，您可以根据需要选择合适的数据库。

## 🗄️ 支持的数据库类型

### 1. SQLite (默认 - 开发环境推荐)
```bash
# .env
DATABASE_URL=sqlite+aiosqlite:///./app.db
```
**特点:**
- ✅ 无需安装数据库服务器
- ✅ 适合开发和测试
- ✅ 开箱即用
- ❌ 不适合高并发生产环境

### 2. PostgreSQL (生产环境推荐)
```bash
# .env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name
```
**特点:**
- ✅ 功能强大，支持复杂查询
- ✅ 优秀的并发性能
- ✅ 丰富的数据类型
- ✅ 适合大型应用

### 3. MySQL (常用选择)
```bash
# .env
DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/database_name
```
**特点:**
- ✅ 广泛使用，生态成熟
- ✅ 良好的性能
- ✅ 易于管理
- ✅ 云服务支持好

## 🔄 切换数据库

### 方法1: 修改环境变量
编辑 `.env` 文件中的 `DATABASE_URL`:
```bash
# 从SQLite切换到PostgreSQL
# DATABASE_URL=sqlite+aiosqlite:///./app.db
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/mydb
```

### 方法2: 使用不同环境配置
```bash
# 开发环境使用SQLite
echo "DATABASE_URL=sqlite+aiosqlite:///./app.db" > .env.dev

# 生产环境使用PostgreSQL
echo "DATABASE_URL=postgresql+asyncpg://user:pass@prod-server:5432/mydb" > .env.prod
```

## 🚀 快速配置示例

### 本地开发 (SQLite)
```bash
# .env
DATABASE_URL=sqlite+aiosqlite:///./app.db
DEBUG=true
```

### 本地开发 (PostgreSQL)
```bash
# .env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/fastapi_dev
DEBUG=true
```

### 本地开发 (MySQL)
```bash
# .env
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/fastapi_dev
DEBUG=true
```

### 生产环境
```bash
# .env.prod
DATABASE_URL=postgresql+asyncpg://prod_user:secure_password@prod-server:5432/fastapi_prod
DEBUG=false
LOG_LEVEL=INFO
```

## 🛠️ 数据库URL格式说明

### PostgreSQL
```
postgresql+asyncpg://[user[:password]@][host][:port][/database]
```

### MySQL
```
mysql+aiomysql://[user[:password]@][host][:port][/database]
```

### SQLite
```
sqlite+aiosqlite:///[path_to_database_file]
```

## 📋 依赖包说明

脚手架已预装所有必要的数据库驱动:
- `aiosqlite` - SQLite异步驱动
- `asyncpg` - PostgreSQL异步驱动
- `aiomysql` - MySQL异步驱动
- `greenlet` - 异步支持库

## 🔧 高级配置

### 连接池配置
在代码中可以调整连接池参数：
```python
# app/providers/database.py
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,        # 连接池大小
    max_overflow=20,     # 最大溢出连接
    pool_timeout=30,     # 获取连接超时
    pool_recycle=3600,   # 连接回收时间
)
```

### SSL连接（生产环境）
```bash
# PostgreSQL with SSL
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db?ssl=require

# MySQL with SSL
DATABASE_URL=mysql+aiomysql://user:pass@host:3306/db?ssl_verify_cert=true
```

## 🚨 注意事项

1. **密码安全**: 生产环境请使用强密码并妥善保管
2. **连接数限制**: 根据数据库服务器配置调整连接池大小
3. **备份策略**: 生产环境务必设置定期备份
4. **监控**: 建议添加数据库性能监控

## 🔍 故障排除

### 常见问题
1. **连接超时**: 检查网络和防火墙设置
2. **认证失败**: 验证用户名密码是否正确
3. **数据库不存在**: 确保数据库已创建
4. **权限不足**: 检查用户权限设置

### 调试技巧
启用SQL日志查看执行的SQL语句：
```python
# 在 database.py 中设置
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 启用SQL日志
)
```
