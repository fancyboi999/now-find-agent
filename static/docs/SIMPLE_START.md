# 🚀 FastAPI Scaffold 超简单入门

## 💡 3步快速启动

### 第1步：准备环境
```bash
# 删除旧环境（如果有）
rm -rf .venv

# 创建新环境
uv venv

# 激活环境
source .venv/bin/activate
```

### 第2步：安装依赖
```bash
# 安装开发版本（推荐）
uv pip install -e ".[dev,database]"

# 或者只安装基础版本
uv pip install -e .
```

### 第3步：启动应用
```bash
# 方式1：直接启动
python main.py

# 方式2：使用make命令
make dev

# 方式3：使用环境切换
./switch-env.sh dev
```

## 🎯 成功标志

看到这些信息说明成功：
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

然后访问：
- 🌐 http://localhost:8000 - 应用主页
- 📖 http://localhost:8000/docs - API文档

## 🔧 常用命令

```bash
# 查看所有命令
make help

# 启动开发服务器
make dev

# 查看版本
make version

# 查看依赖
make deps

# 切换环境
./switch-env.sh dev    # 开发环境
./switch-env.sh test   # 测试环境
```

## 🗄️ 快速配置数据库

编辑 `.env` 文件：

```bash
# SQLite（默认）
DATABASE_URL=sqlite+aiosqlite:///./app.db

# 您的MySQL
DATABASE_URL=mysql+aiomysql://nc_test:nc_test_2019@pc-bp178m3uawx9u46jg.rwlb.rds.aliyuncs.com:3306/now_find

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
```

## 🚨 常见问题

### 问题1：uv 找不到
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

### 问题2：Python版本太低
```bash
# 需要 Python 3.11+
python3 --version
```

### 问题3：依赖安装失败
```bash
# 清理重装
rm -rf .venv
uv venv
source .venv/bin/activate
uv pip install -e ".[dev,database]"
```

### 问题4：应用启动失败
```bash
# 检查配置
cat .env

# 检查导入
python -c "from app.providers import app_provider; print('OK')"
```

## 🎉 就这么简单！

您的 FastAPI 脚手架现在已经可以使用了！

- ✅ 多环境支持（dev/test/uat/prod）
- ✅ 多数据库支持（SQLite/MySQL/PostgreSQL）
- ✅ 现代化项目管理（pyproject.toml）
- ✅ 完整的开发工具链

开始您的开发之旅吧！🚀
