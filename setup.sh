#!/bin/bash

# NOW Find Agent 项目设置脚本
# ==============================

set -e  # 遇到错误时退出

echo "🚀 NOW Find Agent 项目设置"
echo "============================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 Python 版本
check_python() {
    echo -e "${BLUE}📋 检查 Python 版本...${NC}"
    
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 未安装${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    REQUIRED_VERSION="3.11"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
        echo -e "${RED}❌ Python 版本需要 >= 3.11，当前版本: $PYTHON_VERSION${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Python 版本检查通过: $PYTHON_VERSION${NC}"
}

# 检查 uv
check_uv() {
    echo -e "${BLUE}📋 检查 uv 包管理器...${NC}"
    
    if ! command -v uv &> /dev/null; then
        echo -e "${YELLOW}⚠️  uv 未安装，正在安装...${NC}"
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source $HOME/.cargo/env
    fi
    
    echo -e "${GREEN}✅ uv 已安装${NC}"
}

# 创建虚拟环境
create_venv() {
    echo -e "${BLUE}🔧 创建虚拟环境...${NC}"
    
    if [ ! -d ".venv" ]; then
        uv venv
        echo -e "${GREEN}✅ 虚拟环境已创建${NC}"
    else
        echo -e "${YELLOW}⚠️  虚拟环境已存在${NC}"
    fi
}

# 激活虚拟环境
activate_venv() {
    echo -e "${BLUE}🔌 激活虚拟环境...${NC}"
    source .venv/bin/activate
    echo -e "${GREEN}✅ 虚拟环境已激活${NC}"
}

# 安装依赖
install_dependencies() {
    echo -e "${BLUE}📦 安装项目依赖...${NC}"
    
    # 根据用户选择安装不同的依赖组合
    echo "请选择安装类型:"
    echo "1) 基础安装 (仅核心功能)"
    echo "2) 开发安装 (包含开发工具)"
    echo "3) 完整安装 (包含所有功能)"
    echo "4) 自定义安装"
    
    read -p "请输入选择 [1-4]: " choice
    
    case $choice in
        1)
            echo -e "${BLUE}安装基础依赖...${NC}"
            uv pip install -e .
            ;;
        2)
            echo -e "${BLUE}安装开发依赖...${NC}"
            uv pip install -e ".[dev,database]"
            ;;
        3)
            echo -e "${BLUE}安装完整依赖...${NC}"
            uv pip install -e ".[all]"
            ;;
        4)
            echo "可用的依赖组:"
            echo "- database: 数据库驱动"
            echo "- ai: AI/LLM 功能"
            echo "- dev: 开发工具"
            echo "- production: 生产部署"
            echo "- monitoring: 监控工具"
            
            read -p "请输入依赖组 (用逗号分隔): " groups
            uv pip install -e ".[$groups]"
            ;;
        *)
            echo -e "${YELLOW}无效选择，安装基础依赖${NC}"
            uv pip install -e .
            ;;
    esac
    
    echo -e "${GREEN}✅ 依赖安装完成${NC}"
}

# 设置环境配置
setup_env() {
    echo -e "${BLUE}⚙️  设置环境配置...${NC}"
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ 已创建 .env 配置文件${NC}"
        echo -e "${YELLOW}📝 请编辑 .env 文件设置您的配置${NC}"
    else
        echo -e "${YELLOW}⚠️  .env 文件已存在${NC}"
    fi
}

# 数据库设置
setup_database() {
    echo -e "${BLUE}🗄️  数据库设置...${NC}"
    
    echo "请选择数据库类型:"
    echo "1) SQLite (推荐用于开发)"
    echo "2) PostgreSQL"
    echo "3) MySQL"
    echo "4) 跳过，稍后手动配置"
    
    read -p "请输入选择 [1-4]: " db_choice
    
    case $db_choice in
        1)
            echo "DATABASE_URL=sqlite+aiosqlite:///./app.db" >> .env
            echo -e "${GREEN}✅ SQLite 数据库配置完成${NC}"
            ;;
        2)
            read -p "请输入 PostgreSQL 连接信息 (格式: username:password@host:port/database): " pg_info
            echo "DATABASE_URL=postgresql+asyncpg://$pg_info" >> .env
            echo -e "${GREEN}✅ PostgreSQL 数据库配置完成${NC}"
            ;;
        3)
            read -p "请输入 MySQL 连接信息 (格式: username:password@host:port/database): " mysql_info
            echo "DATABASE_URL=mysql+aiomysql://$mysql_info" >> .env
            echo -e "${GREEN}✅ MySQL 数据库配置完成${NC}"
            ;;
        *)
            echo -e "${YELLOW}⚠️  跳过数据库配置${NC}"
            ;;
    esac
}

# 验证安装
verify_installation() {
    echo -e "${BLUE}🧪 验证安装...${NC}"
    
    # 测试导入
    python3 -c "
try:
    from app.providers import app_provider
    from config.config import get_settings
    print('✅ 模块导入测试通过')
except Exception as e:
    print(f'❌ 模块导入测试失败: {e}')
    exit(1)
"
    
    echo -e "${GREEN}✅ 安装验证通过${NC}"
}

# 显示使用说明
show_usage() {
    echo -e "${GREEN}🎉 安装完成！${NC}"
    echo -e "${BLUE}使用说明:${NC}"
    echo ""
    echo "📋 常用命令:"
    echo "  make help          - 查看所有可用命令"
    echo "  make dev           - 启动开发服务器"
    echo "  make test          - 运行测试"
    echo "  make format        - 格式化代码"
    echo ""
    echo "🌍 环境切换:"
    echo "  ./switch-env.sh dev    - 开发环境"
    echo "  ./switch-env.sh test   - 测试环境"
    echo "  ./switch-env.sh uat    - UAT环境"
    echo "  ./switch-env.sh prod   - 生产环境"
    echo ""
    echo "📖 文档:"
    echo "  启动应用后访问: http://localhost:8000/docs"
    echo ""
    echo "🔧 配置文件:"
    echo "  .env               - 环境配置"
    echo "  pyproject.toml     - 项目配置"
    echo ""
}

# 主函数
main() {
    echo -e "${BLUE}开始设置 NOW Find Agent 项目...${NC}"
    echo ""
    
    check_python
    check_uv
    create_venv
    activate_venv
    install_dependencies
    setup_env
    setup_database
    verify_installation
    show_usage
    
    echo -e "${GREEN}🚀 项目设置完成！${NC}"
}

# 运行主函数
main "$@"
