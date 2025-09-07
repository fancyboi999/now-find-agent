# !/usr/bin/python3
"""
功能描述
----------------------------------------------------
@Project :   now-find-agent
@File    :   Paginate.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/7 15:03   zengxinmin@nowcoder.com   1.0         None
"""
from math import ceil

from sqlalchemy.orm import Query

from app.pages.Order import Order


class Paginate:
    items = []
    page_num: int | None = 1
    page_size: int | None = 10
    counts: int | None = 0
    pages: int | None = 0
    orders: list[Order] = None

    def __init__(
        self, query: Query, page_num, page_size, orders: list[Order] | None = None
    ):
        """
        初始化分页参数
        :param query: 查询对象
        :param page_num: 当前页
        :param page_size: 每页数据
        """
        self.query = query
        self.page_num = page_num
        self.page_size = page_size
        self.counts = self.query.count()
        self.pages = ceil(self.counts / self.page_size)
        if (self.page_num - 1) < self.pages:
            offset_num = self.page_size
            self.items = (
                self.query.limit(offset_num)
                .offset((self.page_num - 1) * page_size)
                .all()
            )
        if orders is not None:
            self.orders = orders

    @property
    def next_num(self):
        """下一页"""
        next_num = self.page_num + 1
        if self.page_size < next_num:
            return None
        return next_num

    @property
    def prev_num(self):
        """上一页"""
        prev_num = self.page_size - 1
        if prev_num < 1:
            return None
        return prev_num


if __name__ == "__main__":
    pass
    # paginate = Paginate(query=None, page_num=1, page=10)
    # paginate.items  # 分页后的数据 []
    # paginate.pages  # 共xxx页
    # paginate.page_num  # 当前页码 从1开始
    # paginate.page_size  # 一页几行
    # paginate.prev_num  # 上一页页码
    # paginate.next_num  # 下一页页码
