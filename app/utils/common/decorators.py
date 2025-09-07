import functools
import json
import time
import uuid
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from loguru import logger
from pydantic import BaseModel


def log_request(func: Callable) -> Callable:
    """
    装饰器:记录API请求的详细信息

    可以应用在FastAPI路由函数上,记录请求参数、响应结果和处理时间

    使用方式:
    ```
    @router.post("/endpoint")
    @log_request
    async def my_endpoint(request: SomeModel):
        return {"result": "success"}
    ```
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        # 生成请求ID
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # 获取请求对象并从args中移除,避免序列化问题
        request_obj = None
        filtered_args = []
        for arg in args:
            if isinstance(arg, Request):
                request_obj = arg
            else:
                filtered_args.append(arg)

        # 记录请求信息
        endpoint = func.__name__

        # 格式化请求参数,处理Pydantic模型
        formatted_args = {}
        for key, value in kwargs.items():
            if isinstance(value, BaseModel):
                # 如果是Pydantic模型,转换为字典
                formatted_args[key] = json.loads(value.json())
            elif isinstance(value, Request):
                # 如果是Request对象,只记录基本信息
                formatted_args[key] = f"<Request: {value.method} {value.url.path}>"
            elif hasattr(value, "__dict__"):
                # 对于其他可能无法序列化的对象,使用其字符串表示
                formatted_args[key] = str(value)
            else:
                formatted_args[key] = value

        try:
            # 尝试美化输出参数
            formatted_json = json.dumps(formatted_args, indent=2, ensure_ascii=False)
        except TypeError:
            # 如果JSON序列化失败,使用简单字符串表示
            formatted_json = str(formatted_args)

        # 记录请求路径信息(如果有Request对象)
        path_info = f" | Path: {request_obj.url.path}" if request_obj else ""

        logger.info(
            f"API Request | ID: {request_id} | "
            f"Endpoint: {endpoint}{path_info} | \n"
            f"Args: \n{formatted_json}"
        )

        try:
            # 执行原始函数,确保正确传递Request对象
            if request_obj:
                # 如果有Request对象,需要将其放回参数列表
                response = await func(*filtered_args, request_obj, **kwargs)
            else:
                # 如果没有Request对象,使用过滤后的参数
                response = await func(*filtered_args, **kwargs)

            # 计算处理时间
            process_time = time.time() - start_time

            # 记录响应信息
            logger.info(
                f"API Response | ID: {request_id} | "
                f"Endpoint: {endpoint} | "
                f"Status: Success | "
                f"Duration: {process_time:.4f}s"
            )

            # 如果响应是Response对象,添加请求ID和处理时间
            if isinstance(response, Response):
                response.headers["X-Request-ID"] = request_id
                response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            # 记录异常
            process_time = time.time() - start_time
            logger.error(
                f"API Error | ID: {request_id} | "
                f"Endpoint: {endpoint} | "
                f"Duration: {process_time:.4f}s\n"
                f"Error: \n{e!s}"
            )
            raise

    return wrapper
