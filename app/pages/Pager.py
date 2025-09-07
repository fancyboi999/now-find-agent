# !/usr/bin/python3
"""
分页器类
----------------------------------------------------
@Project :   now-find-agent
@File    :   pager.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/10/25 10:42   zengxinmin@nowcoder.com   1.0         None
"""

from pydantic import BaseModel, Field

from app.utils.core.object_util import ObjectUtil


class Pager(BaseModel):
    """分页数据模型,用于封装分页相关信息"""

    page_num: int | None = Field(title="当前页")
    page_size: int | None = Field(title="每页记录数")
    total_page: int | None = Field(None, title="总页数")
    total_record: int | None = Field(None, title="总记录数")

    @classmethod
    def new(cls, **kwargs):
        """创建分页对象实例"""
        return ObjectUtil.dict_to_obj(kwargs)
