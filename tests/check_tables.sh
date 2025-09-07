#!/bin/bash
"""
快速数据库表结构检查脚本
用于快速验证表结构是否正确初始化
"""

set -e  # 如果任何命令失败则退出

# 脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 进入项目根目录
cd "$PROJECT_ROOT"

echo "=================================================="
echo "🔍 NOW Find Agent - 数据库表结构快速检查"
echo "=================================================="
echo "📍 项目路径: $PROJECT_ROOT"
echo

# 检查是否激活虚拟环境
check_venv() {
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        echo "⚠️  虚拟环境未激活，正在尝试激活..."
        if [[ -f ".venv/bin/activate" ]]; then
            source .venv/bin/activate
            echo "✅ 虚拟环境已激活"
        elif [[ -f "venv/bin/activate" ]]; then
            source venv/bin/activate
            echo "✅ 虚拟环境已激活"
        else
            echo "❌ 未找到虚拟环境，请先创建并激活虚拟环境："
            echo "   uv venv && source .venv/bin/activate"
            exit 1
        fi
    else
        echo "✅ 虚拟环境已激活: $VIRTUAL_ENV"
    fi
}

# 检查环境变量配置
check_env_config() {
    echo
    echo "📋 检查环境配置..."
    
    if [[ -f ".env" ]]; then
        echo "✅ 找到 .env 文件"
        # 显示数据库配置（隐藏密码）
        if grep -q "DATABASE_URL" .env; then
            echo "📊 数据库配置已设置"
        else
            echo "⚠️  未在 .env 中找到 DATABASE_URL 配置，将使用默认 SQLite"
        fi
    else
        echo "⚠️  未找到 .env 文件，将使用默认配置"
    fi
}

# 运行数据库表结构检查
run_table_check() {
    echo
    echo "🔍 运行数据库表结构检查..."
    echo "=================================================="
    
    # 运行Python检查脚本
    python tests/test_database_tables.py
    
    local exit_code=$?
    echo
    if [[ $exit_code -eq 0 ]]; then
        echo "🎉 数据库表结构检查通过！"
    else
        echo "💥 数据库表结构检查失败！"
        echo
        echo "📝 排查建议："
        echo "1. 检查数据库连接配置是否正确"
        echo "2. 确保数据库服务已启动"
        echo "3. 运行应用启动一次以触发表结构创建："
        echo "   python main.py"
        echo "4. 检查应用启动日志中的表结构创建信息"
    fi
    
    return $exit_code
}

# 显示启动应用的方法
show_startup_guide() {
    echo
    echo "=================================================="
    echo "📖 如果表结构未初始化，请按以下步骤启动应用："
    echo "=================================================="
    echo "1. 激活虚拟环境 (如果未激活):"
    echo "   source .venv/bin/activate"
    echo
    echo "2. 启动应用 (这将自动创建表结构):"
    echo "   python main.py"
    echo
    echo "3. 查看启动日志中的表结构创建信息:"
    echo "   应该看到类似以下的日志："
    echo "   '数据库表结构检查完成'"
    echo
    echo "4. 停止应用后再次运行本检查脚本验证"
    echo "=================================================="
}

# 主函数
main() {
    check_venv
    check_env_config
    
    if run_table_check; then
        echo
        echo "✅ 所有检查完成，数据库表结构正常！"
        exit 0
    else
        show_startup_guide
        exit 1
    fi
}

# 运行主函数
main "$@"
