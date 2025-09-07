# FastAPI Scaffold Makefile
# =========================

.PHONY: help install install-dev install-all clean test lint format run dev

# 默认目标
help: ## 显示帮助信息
	@echo "FastAPI Scaffold - 项目管理命令"
	@echo "==============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 环境管理
install: ## 安装核心依赖
	uv pip install -e .

install-dev: ## 安装开发依赖
	uv pip install -e ".[dev]"

install-database: ## 安装数据库驱动
	uv pip install -e ".[database]"

install-ai: ## 安装AI功能依赖
	uv pip install -e ".[ai]"

install-all: ## 安装所有依赖
	uv pip install -e ".[all]"

# 环境管理
env-dev: ## 切换到开发环境
	@export DEPLOY_ENV=dev && echo "🌍 已切换到开发环境"

env-test: ## 切换到测试环境  
	@export DEPLOY_ENV=test && echo "🧪 已切换到测试环境"

env-uat: ## 切换到UAT环境
	@export DEPLOY_ENV=uat && echo "🎯 已切换到UAT环境"

env-prod: ## 切换到生产环境
	@export DEPLOY_ENV=prod && echo "🚀 已切换到生产环境"

# 应用运行
run: ## 运行应用 (生产模式)
	python main.py

dev: ## 运行应用 (开发模式)
	./switch-env.sh dev

test-env: ## 运行应用 (测试环境)
	./switch-env.sh test

uat-env: ## 运行应用 (UAT环境) 
	./switch-env.sh uat

prod-env: ## 运行应用 (生产环境)
	./switch-env.sh prod

# 代码质量
format: ## 格式化代码
	black app/ config/ bootstrap/ tests/
	isort app/ config/ bootstrap/ tests/

lint: ## 代码检查
	flake8 app/ config/ bootstrap/
	mypy app/ config/ bootstrap/

test: ## 运行测试
	pytest tests/ -v

test-cov: ## 运行测试并生成覆盖率报告
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

# 数据库管理
db-upgrade: ## 升级数据库
	@echo "数据库升级功能待实现"

db-downgrade: ## 降级数据库
	@echo "数据库降级功能待实现"

db-reset: ## 重置数据库
	@echo "⚠️  此操作将删除所有数据！"
	@read -p "确认重置数据库? [y/N]: " confirm && [ "$$confirm" = "y" ]
	rm -f app.db uat_app.db

# 项目管理
clean: ## 清理项目
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/

deps: ## 显示依赖信息
	uv pip list

deps-outdated: ## 检查过期依赖
	uv pip list --outdated

# Docker 相关
docker-build: ## 构建Docker镜像
	docker build -t fastapi-scaffold .

docker-run: ## 运行Docker容器
	docker run -p 8000:8000 fastapi-scaffold

# 文档生成
docs: ## 生成API文档
	@echo "启动应用以查看文档:"
	@echo "- Swagger UI: http://localhost:8000/docs"
	@echo "- ReDoc: http://localhost:8000/redoc"

# 安全检查
security: ## 安全检查
	@echo "安全检查功能待实现"
	@echo "建议使用: bandit, safety 等工具"

# 初始化项目
init: ## 初始化新项目
	cp .env.example .env
	@echo "✅ 已创建 .env 配置文件"
	@echo "📝 请编辑 .env 文件设置您的配置"
	@echo "🚀 运行 'make install-dev' 安装开发依赖"

# 快速启动（新手友好）
quick-start: ## 🚀 一键快速启动（新手推荐）
	@echo "🚀 FastAPI Scaffold 快速启动"
	@echo "=============================="
	@echo "📋 检查虚拟环境..."
	@if [ ! -d ".venv" ]; then \
		echo "🔧 创建虚拟环境..."; \
		uv venv; \
	fi
	@echo "📦 安装依赖..."
	@source .venv/bin/activate && uv pip install -e ".[dev,database]"
	@echo "⚙️  检查配置..."
	@if [ ! -f ".env" ]; then \
		cp .env.example .env; \
		echo "✅ 已创建 .env 配置文件"; \
	fi
	@echo "🎉 启动应用..."
	@source .venv/bin/activate && python main.py

# 健康检查
health: ## 应用健康检查
	curl -f http://localhost:8000/health || echo "❌ 应用未运行"

# 版本信息
version: ## 显示版本信息
	@python -c "import tomllib; f=open('pyproject.toml','rb'); config=tomllib.load(f); print('版本:', config['project']['version']); f.close()"
