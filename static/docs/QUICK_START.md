# 🚀 FastAPI Scaffold 快速入门教程

## 📖 什么是 pyproject.toml？

`pyproject.toml` 是 Python 项目的现代化配置文件，它替代了传统的 `requirements.txt` 和 `setup.py`，提供了更强大和标准化的项目管理方式。

## 🎯 5分钟快速上手

### 第一步：检查环境

```bash
# 检查 Python 版本（需要 >= 3.11）
python3 --version

# 检查是否有 uv（推荐的包管理器）
uv --version

# 如果没有 uv，安装它
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 第二步：克隆或初始化项目

```bash
# 如果是新项目
cd /path/to/your/project

# 如果项目已存在
cd /Users/nowcoder/Desktop/now-find-agent
```

### 第三步：一键安装环境

有两种方式，选择其中一种：

#### 方式 A: 使用自动化脚本（推荐新手）
```bash
./setup.sh
```
脚本会引导您完成所有设置！

#### 方式 B: 手动安装（更灵活）
```bash
# 1. 创建虚拟环境
uv venv

# 2. 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或者 Windows: .venv\Scripts\activate

# 3. 安装依赖（选择一种）
uv pip install -e .                    # 基础安装
uv pip install -e ".[dev]"             # 开发安装（推荐）
uv pip install -e ".[dev,database]"    # 开发+数据库
uv pip install -e ".[all]"             # 完整安装

# 4. 复制配置文件
cp .env.example .env
```

### 第四步：启动项目

```bash
# 方式 1: 使用 make 命令（推荐）
make dev

# 方式 2: 使用环境切换脚本
./switch-env.sh dev

# 方式 3: 直接运行
python main.py
```

成功启动后，访问：
- 🌐 应用主页: http://localhost:8000
- 📖 API文档: http://localhost:8000/docs
- 📚 ReDoc文档: http://localhost:8000/redoc

## 🔧 常用命令速查

### 项目管理命令

```bash
make help          # 📋 查看所有可用命令
make version       # 📌 显示项目版本
make deps          # 📦 显示已安装的依赖
make clean         # 🧹 清理项目临时文件
```

### 开发相关命令

```bash
make dev           # 🚀 启动开发服务器
make test          # 🧪 运行测试
make format        # ✨ 格式化代码
make lint          # 🔍 代码检查
```

### 环境管理命令

```bash
make env-dev       # 🔧 切换到开发环境
make env-test      # 🧪 切换到测试环境
make env-uat       # 🎯 切换到UAT环境
make env-prod      # 🚀 切换到生产环境
```

### 依赖管理命令

```bash
make install              # 📦 安装核心依赖
make install-dev          # 🛠️ 安装开发依赖
make install-database     # 🗄️ 安装数据库驱动
make install-ai           # 🤖 安装AI功能
make install-all          # 🎯 安装所有功能
```

## 🌍 环境切换详解

### 方法 1: 使用切换脚本（推荐）

```bash
./switch-env.sh dev     # 开发环境（默认SQLite）
./switch-env.sh test    # 测试环境（内存数据库）
./switch-env.sh uat     # UAT环境（生产级数据库）
./switch-env.sh prod    # 生产环境（生产级数据库）
```

### 方法 2: 使用环境变量

```bash
export DEPLOY_ENV=dev
python main.py
```

### 方法 3: 使用 make 命令

```bash
make dev           # 等同于 ./switch-env.sh dev
make test-env      # 等同于 ./switch-env.sh test
make uat-env       # 等同于 ./switch-env.sh uat
make prod-env      # 等同于 ./switch-env.sh prod
```

## 🗄️ 数据库配置

### 快速配置不同数据库

编辑 `.env` 文件中的 `DATABASE_URL`：

```bash
# SQLite（开发推荐）
DATABASE_URL=sqlite+aiosqlite:///./app.db

# PostgreSQL（生产推荐）
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database

# MySQL
DATABASE_URL=mysql+aiomysql://username:password@localhost:3306/database

# 您的MySQL配置示例
DATABASE_URL=mysql+aiomysql://nc_test:nc_test_2019@pc-bp178m3uawx9u46jg.rwlb.rds.aliyuncs.com:3306/now_find
```

系统会自动检测数据库类型并应用最佳配置！

## 📦 依赖组说明

我们的 pyproject.toml 将依赖分为几个组：

```bash
# 核心依赖（自动安装）
- fastapi          # Web框架
- uvicorn          # ASGI服务器  
- pydantic         # 数据验证
- sqlalchemy       # ORM
- redis            # 缓存

# 可选依赖组
[database]         # 数据库驱动（MySQL、PostgreSQL、SQLite）
[ai]              # AI/LLM功能（LangChain、OpenAI等）
[dev]             # 开发工具（pytest、black、mypy等）
[production]      # 生产部署工具
[monitoring]      # 监控工具
[all]             # 包含所有功能
```

### 按需安装示例

```bash
# 只需要基础功能
uv pip install -e .

# 需要开发工具
uv pip install -e ".[dev]"

# 需要数据库支持
uv pip install -e ".[dev,database]"

# 需要AI功能
uv pip install -e ".[dev,database,ai]"

# 需要全部功能
uv pip install -e ".[all]"
```

## 🔧 配置文件详解

### 环境配置优先级

```
1. 环境变量（最高优先级）
2. .env.{环境}文件（如 .env.dev）
3. .env 文件
4. 代码默认值（最低优先级）
```

### 配置文件说明

```bash
.env              # 基础配置，所有环境共享
.env.dev          # 开发环境特定配置
.env.test         # 测试环境配置
.env.uat          # UAT环境配置  
.env.prod         # 生产环境配置
.env.example      # 配置模板（不要直接修改）
```

## 🚨 常见问题解决

### 问题1: Python 版本不对
```bash
# 错误信息：requires-python = ">=3.11"
# 解决方案：升级 Python 到 3.11+
pyenv install 3.11.9
pyenv global 3.11.9
```

### 问题2: uv 命令找不到
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # 或重新打开终端
```

### 问题3: 虚拟环境问题
```bash
# 删除现有虚拟环境重新创建
rm -rf .venv
uv venv
source .venv/bin/activate
```

### 问题4: 依赖安装失败
```bash
# 清理缓存重新安装
uv cache clean
uv pip install -e ".[dev]" --no-cache
```

### 问题5: 应用启动失败
```bash
# 检查配置文件
cat .env

# 检查数据库连接
make health

# 查看详细错误
python main.py
```

## 💡 开发流程建议

### 日常开发流程

```bash
# 1. 激活环境
source .venv/bin/activate

# 2. 拉取最新代码
git pull

# 3. 更新依赖（如果有变化）
uv pip install -e ".[dev]"

# 4. 启动开发服务器
make dev

# 5. 开发完成后运行测试
make test

# 6. 格式化代码
make format

# 7. 代码检查
make lint
```

### 新功能开发

```bash
# 1. 创建新分支
git checkout -b feature/new-feature

# 2. 开发新功能
make dev

# 3. 添加测试
# 编辑 tests/ 目录下的测试文件

# 4. 运行测试确保通过
make test

# 5. 提交代码
git add .
git commit -m "feat: 添加新功能"
```

## 🎯 小贴士

1. **使用 make help** 查看所有可用命令
2. **定期运行 make format** 保持代码格式一致
3. **开发时使用 make dev** 获得热重载
4. **部署前运行 make test** 确保测试通过
5. **查看 API 文档** 访问 http://localhost:8000/docs

## 🚀 恭喜！

您已经掌握了 FastAPI Scaffold 的基本使用方法！

现在您可以：
- ✅ 快速启动项目
- ✅ 切换不同环境  
- ✅ 管理项目依赖
- ✅ 使用开发工具

开始您的 FastAPI 开发之旅吧！🎉
