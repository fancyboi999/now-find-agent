# !/usr/bin/python3
"""
功能描述
----------------------------------------------------
@Project :   now-find-agent
@File    :   BaseTenantEntity.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2025-09-05   zengxinmin   1.0         None
"""

from sqlalchemy import Column, Integer

from app.orm.entity.BaseEntity import BaseEntity


class BaseTenantEntity(BaseEntity):
    """
    实体基类(持久化模型由此类继承)
    """

    __abstract__ = True  ## 声明当前类为抽象类,被继承,调用不会被创建
    tenant_id = Column(Integer, comment="租户ID")
