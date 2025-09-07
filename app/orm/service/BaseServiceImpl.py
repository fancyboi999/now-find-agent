# !/usr/bin/python3
"""
功能描述
----------------------------------------------------
@Project :   now-find-agent
@File    :   BaseService.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2025-09-05   zengxinmin   1.0         None
"""
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm.dao.BaseDao import BaseDao
from app.pages.Order import Order
from app.pages.PageHelper import PageHelper
from app.pages.Paginate import Paginate

M = TypeVar("M", bound=BaseModel)


class BaseServiceImpl(Generic[M]):
    """
    基础Service服务类
    """

    db: AsyncSession
    dao: BaseDao = None
    cls = None

    def __init__(self, db: AsyncSession, cls=None, dao: BaseDao = None):
        self.db = db  # 这行缺失了
        if cls is not None:
            # 如果实例化时不传递实体cls类型,则需要手动调用query(User)方法将模型cls传入
            self.cls = cls
        if dao is not None:
            self.dao = dao
        else:
            self.dao = BaseDao(self.db, cls)

    def query(self, cls):
        """
        设置查询模型
        """
        if cls is not None:
            # 如果实例化时不传递实体cls类型,则需要手动调用query(User)方法将模型cls传入
            self.cls = cls
        return self

    async def save(self, model: M) -> M:
        """
        根据模型保存数据
        """
        return await self.dao.save(model)

    async def save_not_commit(self, model: M) -> M:
        """
        根据模型保存数据
        """
        return await self.dao.save_not_commit(model)

    async def save_all(self, models: list[M]) -> bool:
        """
        批量模型保存数据
        """
        return await self.dao.save_all(models)

    async def save_all_not_commit(self, models: list[M]) -> bool:
        """
        批量模型保存数据
        """
        return await self.dao.save_all_not_commit(models)

    async def update(self, model: M) -> M:
        """
        根据模型更新数据
        """
        return await self.dao.update(model)

    async def update_not_commit(self, model: M) -> M:
        """
        根据模型更新数据
        """
        return await self.dao.update_not_commit(model)

    async def update_all(self, models: list[M]) -> bool:
        """
        批量模型更新数据
        """
        return await self.dao.update_all(models)

    async def update_all_not_commit(self, models: list[M]) -> bool:
        """
        批量模型更新数据
        """
        return await self.dao.update_all_not_commit(models)

    async def delete(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        return await self.dao.delete(model)

    async def delete_by_id(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        return await self.dao.delete_by_id(model)

    async def delete_all(self, models: list[M]):
        """
        批量根据模型删除数据
        """
        return await self.dao.delete_all(models)

    async def exists(self, model: M) -> bool:
        """
        根据模型查询判断数据是否存在
        """
        return await self.dao.exists(model)

    async def count(self, model: M) -> int:
        """
        根据模型统计数据条数
        """
        return await self.dao.count(model)

    async def find_by_id(self, model: M) -> M:
        """
        根据模型查询指定ID数据
        """
        return await self.dao.find_by_id(model)

    async def find_by_ids(self, ids: list[int], model: M = None) -> list[M]:
        """
        根据模型查询指定ID数据
        """
        return await self.dao.find_by_ids(ids, model)

    async def find_all(self, model: M, order: Order = None) -> list[M]:
        """
        根据模型查询所有数据
        """
        return await self.dao.find_all(model, order)

    async def find_by(self, search: PageHelper[M]) -> Paginate:
        """
        根据模型查询分页数据
        """
        return await self.dao.find_by(search)
