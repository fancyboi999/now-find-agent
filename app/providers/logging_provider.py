import logging
import os

from fastapi import FastAPI, Request
from loguru import logger

from config.config import DevelopmentSettings, ProductionSettings

# 添加全局标志防止重复配置
_LOGGER_CONFIGURED = False


class InterceptHandler(logging.Handler):
    """拦截 fastapi 主程序的 log

    Args:
        logging (_type_): _description_
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # type: ignore
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def register(app: FastAPI, settings: DevelopmentSettings | ProductionSettings) -> None:
    # 使用全局标志防止重复配置
    global _LOGGER_CONFIGURED
    if _LOGGER_CONFIGURED:
        return

    # 只使用最简单的控制台日志,完全避免多进程问题
    # 避免使用loguru的多进程处理器
    import sys

    # 清除所有处理程序
    logger.remove()

    # 确保日志目录存在
    # 处理loguru的格式化字符串,将双大括号替换为单大括号
    log_path = settings.LOG_PATH.replace("{time:", "{")
    error_log_path = settings.LOG_PATH_ERROR.replace("{time:", "{")

    log_dir = os.path.dirname(log_path.replace("{YYYY-MM-DD}", ""))
    error_log_dir = os.path.dirname(error_log_path.replace("{YYYY-MM-DD}", ""))

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(error_log_dir, exist_ok=True)

    # 添加控制台日志处理程序
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <4}</level> | <cyan>using_function:{function}</cyan> | <cyan>{file}:{line}</cyan> | <level>{message}</level>",
        colorize=True,
    )

    # 添加普通文件日志处理程序
    logger.add(
        settings.LOG_PATH,
        level=settings.LOG_LEVEL,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <4}</level> | <cyan>using_function:{function}</cyan> | <cyan>{file}:{line}</cyan> | <level>{message}</level>",
        encoding="utf-8",
    )

    # 添加错误日志文件处理程序
    logger.add(
        settings.LOG_PATH_ERROR,
        level=settings.LOG_LEVEL_ERROR,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <4}</level> | <cyan>using_function:{function}</cyan> | <cyan>{file}:{line}</cyan> | <level>{message}</level>",
        encoding="utf-8",
    )

    # 添加json格式日志文件(可选,用于ELK或其他日志分析系统)
    # logger.add(
    #     settings.LOG_PATH.replace(".log", ".json"),
    #     level=settings.LOG_LEVEL,
    #     rotation=settings.LOG_ROTATION,
    #     retention=settings.LOG_RETENTION,
    #     format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {line} | {message}",
    #     serialize=True,  # 启用JSON序列化
    # )

    # 设置为全局日志处理程序
    app.state.logger = logger

    # 添加日志中间件
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        import json
        import time
        import uuid

        request_id = str(uuid.uuid4())
        start_time = time.time()

        # 获取请求的详细信息
        client_host = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"
        server_host = request.url.hostname or "unknown"
        server_port = request.url.port or "unknown"

        # 获取查询参数
        query_params = dict(request.query_params) if request.query_params else {}

        # 获取路径参数
        path_params = (
            dict(request.path_params) if hasattr(request, "path_params") else {}
        )

        # 获取请求头(过滤敏感信息)
        headers = dict(request.headers)
        # 过滤敏感的请求头
        sensitive_headers = ["authorization", "cookie", "x-api-key", "x-auth-token"]
        filtered_headers = {
            k: v if k.lower() not in sensitive_headers else "***"
            for k, v in headers.items()
        }

        # 尝试获取请求体(仅对POST/PUT/PATCH请求)
        request_body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                # 读取请求体
                body = await request.body()
                if body:
                    # 尝试解析JSON
                    try:
                        request_body = json.loads(body.decode("utf-8"))
                        # 过滤敏感字段
                        if isinstance(request_body, dict):
                            sensitive_fields = ["password", "secret", "token", "key"]
                            for field in sensitive_fields:
                                if field in request_body:
                                    request_body[field] = "***"
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        request_body = f"<binary data: {len(body)} bytes>"
            except Exception as e:
                request_body = f"<error reading body: {e!s}>"

        # 记录详细的请求开始信息
        logger.info(
            f"🚀 请求开始 [{request.method}] {request.url.path} - ID: {request_id}\n"
            f"   📍 客户端: {client_host}:{client_port} -> 服务端: {server_host}:{server_port}\n"
            f"   🔗 完整URL: {request.url!s}\n"
            f"   📋 查询参数: {query_params}\n"
            f"   🛤️  路径参数: {path_params}\n"
            f"   📤 请求头: {filtered_headers}\n"
            f"   📦 请求体: {request_body}"
        )

        # 执行请求
        response = await call_next(request)

        # 计算处理时间
        process_time = time.time() - start_time

        # 记录请求结束和响应状态
        logger.info(
            f"✅ 请求完成 [{request.method}] {request.url.path} - ID: {request_id}\n"
            f"   📊 状态码: {response.status_code}\n"
            f"   ⏱️  处理耗时: {process_time:.4f}秒\n"
            f"   📍 客户端: {client_host}:{client_port}"
        )

        return response

    # 设置标志,表示日志已配置
    _LOGGER_CONFIGURED = True
