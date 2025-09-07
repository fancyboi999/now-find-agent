# !/usr/bin/python3
"""
功能描述
----------------------------------------------------
@Project :   now-find-agent
@File    :   Sorter.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2025-09-05   zengxinmin   1.0         None
"""

from pydantic import BaseModel, Field
from pydantic.v1 import Required

from app.pages.Order import Order


class Sorter(BaseModel):
    orders: list[Order] | None = Field(default=Required, title="排序条件集合")

    @classmethod
    def new(cls, **kwargs):
        orders_list: list[Order] = []
        for order in kwargs.get("orders"):
            orders_list.append(Order.new(**order))
        return Sorter(orders_list)
