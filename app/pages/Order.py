# !/usr/bin/python3
"""
排序类 - 用于处理数据排序
----------------------------------------------------
@Project :   now-find-agent
@File    :   order.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2025-09-05   zengxinmin   1.0         None
"""

from pydantic import BaseModel, Field

from app.utils.core.object_util import ObjectUtil


class Order(BaseModel):
    """排序数据模型,用于封装排序相关信息"""

    property: str | None = Field(None, title="排序字段")
    direction: str | None = Field(
        None, title="排序条件", description="排序:asc=升序,desc=降序"
    )

    @classmethod
    def new(cls, **kwargs):
        """创建排序对象实例"""
        return ObjectUtil.dict_to_obj(kwargs)
