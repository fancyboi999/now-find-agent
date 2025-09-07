import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.providers.logging_provider import logger


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """
    中间件:记录请求日志,包括请求路径、方法、处理时间、状态码等信息
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # 记录请求开始
        logger.info(
            f"Request started | ID: {request_id} | "
            f"Method: {request.method} | Path: {request.url.path} | "
            f"Client: {request.client.host if request.client else 'Unknown'}"
        )

        try:
            # 处理请求
            response = await call_next(request)

            # 计算处理时间
            process_time = time.time() - start_time

            # 记录请求结束
            logger.info(
                f"Request completed | ID: {request_id} | "
                f"Method: {request.method} | Path: {request.url.path} | "
                f"Status: {response.status_code} | "
                f"Duration: {process_time:.4f}s"
            )

            # 添加自定义响应头,包含请求ID和处理时间
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            # 记录异常
            process_time = time.time() - start_time
            logger.error(
                f"Request failed | ID: {request_id} | "
                f"Method: {request.method} | Path: {request.url.path} | "
                f"Error: {e!s} | Duration: {process_time:.4f}s"
            )
            raise
