# !/usr/bin/python3
"""
功能描述
----------------------------------------------------
@Project :   now-find-agent
@File    :   PageHelper.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:17   zengxinmin@nowcoder.com   1.0         None
"""
from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.v1 import Required

from app.pages.Pager import Pager
from app.pages.Sorter import Sorter

M = TypeVar("M")


class PageHelper(BaseModel, Generic[M]):
    """
    分页查询条件
    """

    query: M | None = Field(default=Required, title="查询条件")
    pager: Pager | None = Field(default=Required, title="分页条件")
    sorter: Sorter | None = Field(default=None, title="排序条件")


class PageResultHelper(BaseModel, Generic[M]):
    """
    分页查询返回结果
    """

    content: list[M] | None = Field(default=Required, title="返回数据集合")
    pager: Pager | None = Field(default=Required, title="分页条件")
    sorter: Sorter | None = Field(default=None, title="排序条件")
