#!/usr/bin/env python3
"""
数据库表结构验证脚本
验证表结构是否正确初始化以及字段完整性
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError, InvalidRequestError

from app.models.Agent import Agent
from app.models.LLM import LLM
from app.models.Tool import Tool
from app.providers.database import async_session, DB_TYPE, SCHEMA_NAME, engine


class DatabaseTableChecker:
    """数据库表结构检查器"""
    
    def __init__(self):
        self.expected_tables = {
            'agent': Agent,
            'llm': LLM,
            'tool': Tool
        }
        self.results = {
            'database_type': DB_TYPE,
            'schema_name': SCHEMA_NAME,
            'tables_status': {},
            'overall_status': False,
            'errors': []
        }

    async def check_database_connection(self) -> bool:
        """检查数据库连接"""
        try:
            async with async_session() as session:
                await session.execute(text("SELECT 1"))
            logger.info("✅ 数据库连接正常")
            return True
        except Exception as e:
            logger.error(f"❌ 数据库连接失败: {e}")
            self.results['errors'].append(f"数据库连接失败: {e}")
            return False

    async def get_existing_tables(self) -> list:
        """获取数据库中现有的表"""
        try:
            async with engine.begin() as conn:
                # 使用 run_sync 来运行同步的 inspect 操作
                def get_table_names(sync_conn):
                    inspector = inspect(sync_conn)
                    return inspector.get_table_names()
                
                tables = await conn.run_sync(get_table_names)
            
            logger.info(f"📋 数据库中现有表: {tables}")
            return tables
        except Exception as e:
            logger.error(f"❌ 获取表列表失败: {e}")
            self.results['errors'].append(f"获取表列表失败: {e}")
            return []

    async def check_table_structure(self, table_name: str, model_class) -> dict:
        """检查单个表的结构"""
        table_status = {
            'exists': False,
            'columns': {},
            'expected_columns': {},
            'missing_columns': [],
            'extra_columns': [],
            'column_mismatches': []
        }
        
        try:
            # 获取模型期望的列
            expected_columns = {}
            for column_name, column in model_class.__table__.columns.items():
                expected_columns[column_name] = {
                    'type': str(column.type),
                    'nullable': column.nullable,
                    'primary_key': column.primary_key,
                    'unique': column.unique,
                    'comment': column.comment
                }
            
            table_status['expected_columns'] = expected_columns
            
            # 获取实际的表结构
            async with engine.begin() as conn:
                def get_table_info(sync_conn):
                    inspector = inspect(sync_conn)
                    try:
                        return inspector.get_columns(table_name)
                    except Exception:
                        return None
                
                columns_info = await conn.run_sync(get_table_info)
            
            if columns_info is None:
                table_status['exists'] = False
                table_status['missing_columns'] = list(expected_columns.keys())
                return table_status
            
            table_status['exists'] = True
            
            # 分析列信息
            actual_columns = {}
            for col_info in columns_info:
                col_name = col_info['name']
                actual_columns[col_name] = {
                    'type': str(col_info['type']),
                    'nullable': col_info['nullable'],
                    'comment': col_info.get('comment', '')
                }
            
            table_status['columns'] = actual_columns
            
            # 检查缺失和多余的列
            expected_cols = set(expected_columns.keys())
            actual_cols = set(actual_columns.keys())
            
            table_status['missing_columns'] = list(expected_cols - actual_cols)
            table_status['extra_columns'] = list(actual_cols - expected_cols)
            
            logger.info(f"✅ 表 '{table_name}' 结构检查完成")
            
        except Exception as e:
            logger.error(f"❌ 检查表 '{table_name}' 结构失败: {e}")
            self.results['errors'].append(f"检查表 '{table_name}' 结构失败: {e}")
        
        return table_status

    async def run_full_check(self) -> dict:
        """运行完整的表结构检查"""
        logger.info("🔍 开始数据库表结构验证...")
        logger.info(f"📊 数据库类型: {DB_TYPE}")
        logger.info(f"📊 Schema名称: {SCHEMA_NAME}")
        
        # 1. 检查数据库连接
        if not await self.check_database_connection():
            self.results['overall_status'] = False
            return self.results
        
        # 2. 获取现有表
        await self.get_existing_tables()
        
        # 3. 检查每个期望的表
        all_tables_ok = True
        for table_name, model_class in self.expected_tables.items():
            logger.info(f"\n🔍 检查表: {table_name}")
            table_status = await self.check_table_structure(table_name, model_class)
            self.results['tables_status'][table_name] = table_status
            
            # 判断表状态
            if not table_status['exists']:
                logger.error(f"❌ 表 '{table_name}' 不存在")
                all_tables_ok = False
            elif table_status['missing_columns']:
                logger.warning(f"⚠️ 表 '{table_name}' 缺少列: {table_status['missing_columns']}")
                all_tables_ok = False
            elif table_status['extra_columns']:
                logger.info(f"ℹ️ 表 '{table_name}' 有额外列: {table_status['extra_columns']}")
            else:
                logger.info(f"✅ 表 '{table_name}' 结构正常")
        
        self.results['overall_status'] = all_tables_ok
        
        return self.results

    def print_summary(self):
        """打印检查结果摘要"""
        print("\n" + "="*80)
        print("📊 数据库表结构验证报告")
        print("="*80)
        print(f"数据库类型: {self.results['database_type']}")
        print(f"Schema名称: {self.results['schema_name']}")
        print(f"总体状态: {'✅ 正常' if self.results['overall_status'] else '❌ 异常'}")
        
        print(f"\n📋 表状态明细:")
        for table_name, status in self.results['tables_status'].items():
            exists_icon = "✅" if status['exists'] else "❌"
            print(f"  {exists_icon} {table_name}")
            
            if status['missing_columns']:
                print(f"    ⚠️ 缺少列: {', '.join(status['missing_columns'])}")
            if status['extra_columns']:
                print(f"    ℹ️ 额外列: {', '.join(status['extra_columns'])}")
            if status['exists'] and not status['missing_columns']:
                print(f"    📊 列数: {len(status['columns'])}")
        
        if self.results['errors']:
            print("\n❌ 错误列表:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        print("\n" + "="*80)


async def main():
    """主函数"""
    checker = DatabaseTableChecker()
    
    try:
        results = await checker.run_full_check()
        checker.print_summary()
        
        # 根据检查结果返回不同的退出码
        if results['overall_status']:
            logger.info("🎉 数据库表结构验证通过!")
            return 0
        else:
            logger.error("💥 数据库表结构验证失败!")
            return 1
            
    except Exception as e:
        logger.error(f"💥 验证过程出现异常: {e}")
        return 1


if __name__ == "__main__":
    # 设置日志级别
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="<green>{time}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
