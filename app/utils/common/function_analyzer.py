"""
函数分析工具
用于分析函数长度和复杂度,帮助重构决策
"""

import ast
from typing import NamedTuple

from loguru import logger


class FunctionInfo(NamedTuple):
    """函数信息"""

    name: str
    start_line: int
    end_line: int
    line_count: int
    complexity_score: int


class FunctionAnalyzer:
    """函数分析器类"""

    @staticmethod
    def analyze_file(file_path: str) -> list[FunctionInfo]:
        """
        分析文件中的所有函数

        Args:
            file_path: 文件路径

        Returns:
            函数信息列表
        """
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        try:
            tree = ast.parse(content)
            analyzer = FunctionAnalyzer()
            return analyzer._extract_functions(tree)
        except SyntaxError as e:
            logger.info(f"语法错误: {e}")
            return []

    def _extract_functions(self, tree: ast.AST) -> list[FunctionInfo]:
        """提取函数信息"""
        functions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                # 计算函数行数
                start_line = node.lineno
                end_line = self._get_end_line(node)
                line_count = end_line - start_line + 1

                # 计算复杂度分数
                complexity = self._calculate_complexity(node)

                functions.append(
                    FunctionInfo(
                        name=node.name,
                        start_line=start_line,
                        end_line=end_line,
                        line_count=line_count,
                        complexity_score=complexity,
                    )
                )

        return sorted(functions, key=lambda x: x.line_count, reverse=True)

    def _get_end_line(self, node: ast.AST) -> int:
        """获取函数结束行号"""
        end_line = node.lineno
        for child in ast.walk(node):
            if hasattr(child, "lineno") and child.lineno > end_line:
                end_line = child.lineno
        return end_line

    def _calculate_complexity(self, node: ast.AST) -> int:
        """
        计算函数复杂度分数

        基于以下因素:
        - if/elif/else 语句
        - for/while 循环
        - try/except 块
        - 嵌套深度
        """
        complexity = 1  # 基础复杂度

        for child in ast.walk(node):
            if isinstance(child, ast.If | ast.For | ast.While | ast.Try):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1

        return complexity

    @staticmethod
    def get_refactor_suggestions(functions: list[FunctionInfo]) -> dict[str, str]:
        """
        获取重构建议

        Args:
            functions: 函数信息列表

        Returns:
            重构建议字典
        """
        suggestions = {}

        for func in functions:
            if func.line_count > 50:
                suggestions[func.name] = "函数过长,建议拆分为多个小函数"
            elif func.complexity_score > 10:
                suggestions[func.name] = "函数复杂度过高,建议简化逻辑"
            elif func.line_count > 30 and func.complexity_score > 5:
                suggestions[func.name] = "函数长度和复杂度都较高,建议重构"

        return suggestions


def analyze_and_suggest(file_path: str) -> None:
    """
    分析文件并提供重构建议

    Args:
        file_path: 要分析的文件路径
    """
    logger.info(f"🔍 分析文件: {file_path}")
    logger.info("=" * 60)

    functions = FunctionAnalyzer.analyze_file(file_path)
    suggestions = FunctionAnalyzer.get_refactor_suggestions(functions)

    logger.info("📊 函数统计 (按行数排序):")
    logger.info(f"{'函数名':<30} {'行数':<8} {'复杂度':<8} {'起始行':<8}")
    logger.info("-" * 60)

    for func in functions:
        logger.info(
            f"{func.name:<30} {func.line_count:<8} {func.complexity_score:<8} {func.start_line:<8}"
        )

    if suggestions:
        logger.info("\n💡 重构建议:")
        logger.info("-" * 40)
        for func_name, suggestion in suggestions.items():
            logger.info(f"• {func_name}: {suggestion}")
    else:
        logger.info("\n✅ 所有函数长度和复杂度都在合理范围内")


if __name__ == "__main__":
    # 示例用法
    analyze_and_suggest("app/services/state_service.py")
