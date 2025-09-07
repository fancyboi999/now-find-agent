#!/bin/bash

# FastAPI 多环境切换工具
# =======================

ENV=${1:-dev}
VALID_ENVS=("dev" "test" "uat" "prod")

# 检查参数
if [[ ! " ${VALID_ENVS[@]} " =~ " ${ENV} " ]]; then
    echo "❌ 无效的环境: $ENV"
    echo "✅ 支持的环境: ${VALID_ENVS[*]}"
    echo ""
    echo "用法: ./switch-env.sh [dev|test|uat|prod]"
    exit 1
fi

# 检查配置文件是否存在
ENV_FILE=".env.$ENV"
if [[ ! -f "$ENV_FILE" ]]; then
    echo "⚠️  配置文件不存在: $ENV_FILE"
    echo "📋 请创建该文件或使用现有环境"
    exit 1
fi

# 设置环境变量
export DEPLOY_ENV=$ENV

# 显示环境信息
echo "🌍 环境切换信息"
echo "==============="
echo "🎯 目标环境: $ENV"
echo "📁 配置文件: .env + $ENV_FILE"
echo "🔧 环境变量: DEPLOY_ENV=$ENV"

# 显示数据库配置预览
if grep -q "DATABASE_URL" "$ENV_FILE"; then
    DB_URL=$(grep "^DATABASE_URL" "$ENV_FILE" | head -1 | cut -d'=' -f2-)
    DB_TYPE="Unknown"
    if [[ $DB_URL == *"sqlite"* ]]; then
        DB_TYPE="SQLite"
    elif [[ $DB_URL == *"postgresql"* ]]; then
        DB_TYPE="PostgreSQL"
    elif [[ $DB_URL == *"mysql"* ]]; then
        DB_TYPE="MySQL"
    fi
    echo "🗄️  数据库类型: $DB_TYPE"
fi

echo ""
echo "🚀 启动应用..."
echo "==============="

# 启动应用
python main.py
