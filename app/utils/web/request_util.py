# !/usr/bin/python3
"""
HTTP请求工具类 - 提供简化的HTTP请求功能
----------------------------------------------------
@Project :   now-find-agent
@File    :   request_util.py
@Contact :   sp_hrz@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/11 13:22   shenpeng   1.0         None
"""
from typing import Any

import requests
from fastapi import Request
from loguru import logger

from app.utils.object_dict import ObjectDict


class RequestUtil:
    """HTTP请求工具类,提供链式调用的HTTP请求方法"""

    def __init__(self, base_url: str):
        """
        初始化RequestUtil对象

        Args:
            base_url: 基础URL,用于构建完整请求URL
        """
        # 确保URL以http://或https://开头
        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            base_url = f"http://{base_url}"

        self.base_url = base_url
        self.headers: dict[str, str] = {}
        self.convert_underscores: bool = False
        self.timeout: int | None = None

    def set_headers(
        self, headers_list: list[dict[str, Any]], convert_underscores: bool = True
    ) -> "RequestUtil":
        """
        设置请求头

        Args:
            headers_list: 包含多个字典形式的请求头的列表
            convert_underscores: 是否将参数键名中的下划线替换为连字符

        Returns:
            RequestUtil实例,支持链式调用
        """
        self.convert_underscores = convert_underscores

        for header_dict in headers_list:
            for key, value in header_dict.items():
                new_key = key.replace("_", "-") if self.convert_underscores else key
                # 将值转换为字符串类型
                str_value = str(value) if not isinstance(value, str | bytes) else value
                self.headers[new_key] = str_value
        return self

    def set_timeout(self, timeout: int) -> "RequestUtil":
        """
        设置请求超时时间

        Args:
            timeout: 请求超时时间(秒)

        Returns:
            RequestUtil实例,支持链式调用
        """
        self.timeout = timeout
        return self

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> requests.Response:
        """
        发送GET请求

        Args:
            endpoint: 请求路径
            params: 查询参数

        Returns:
            HTTP响应对象
        """
        url = self.base_url + endpoint
        response = requests.get(
            url, params=params, headers=self.headers, timeout=self.timeout
        )
        return response

    def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> requests.Response:
        """
        发送POST请求

        Args:
            endpoint: 请求路径
            data: 表单数据
            json: JSON数据

        Returns:
            HTTP响应对象
        """
        url = self.base_url + endpoint
        response = requests.post(
            url, data=data, json=json, headers=self.headers, timeout=self.timeout
        )
        return response

    def put(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> requests.Response:
        """
        发送PUT请求

        Args:
            endpoint: 请求路径
            data: 表单数据
            json: JSON数据

        Returns:
            HTTP响应对象
        """
        url = self.base_url + endpoint
        response = requests.put(
            url, data=data, json=json, headers=self.headers, timeout=self.timeout
        )
        return response

    def delete(self, endpoint: str) -> requests.Response:
        """
        发送DELETE请求

        Args:
            endpoint: 请求路径

        Returns:
            HTTP响应对象
        """
        url = self.base_url + endpoint
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        return response


# 示例用法
if __name__ == "__main__":
    # 简单登录示例
    response = RequestUtil("http://127.0.0.1:8848").post(
        "/nacos/v1/auth/login", {"username": "nacos", "password": "nacos"}
    )
    response_data = response.json()
    result_object = ObjectDict.from_dict(response_data)
    logger.info(result_object)

    # 以下是更复杂的请求示例(已注释)
    """
    base_url = "http://api.example.com"
    request_client = RequestUtil(base_url)

    # 设置请求头和发送POST请求
    headers = [
        {"tenant-id": "888888"},
        {"classify-type": "role"},
        {"classify-id": "888888"},
        {"platform-code": "pt"}
    ]

    response = request_client.set_headers(headers).post(
        "/auth/login",
        json={
            "username": "user123",
            "password": "password123"
        }
    )
    response_data = response.json()
    result_object = ObjectDict.from_dict(response_data)
    logger.info(result_object)

    # 发送PUT请求更新数据
    payload = {"status": "active"}
    response = request_client.put("/users/123", json=payload)

    # 设置超时并发送DELETE请求
    response = request_client.set_timeout(10).delete("/users/123")
    """


def get_request_source(request: Request) -> str | None:
    """
    从请求头中获取请求来源

    Args:
        request: FastAPI的Request对象

    Returns:
        请求来源的URL,如果不存在则返回None
    """
    return request.headers.get("origin") or request.headers.get("referer")
