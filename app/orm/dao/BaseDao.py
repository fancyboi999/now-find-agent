# !/usr/bin/python3
"""
功能描述
----------------------------------------------------
@Project :   now-find-agent
@File    :   BaseDao.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/2/6 10:47   zengxinmin@nowcoder.com   1.0         None
"""
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import desc, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.pages.Order import Order
from app.pages.PageHelper import PageHelper
from app.pages.Paginate import Paginate

M = TypeVar("M", bound=BaseModel)


class BaseDao(Generic[M]):
    """
    基础Dao服务类
    """

    db: AsyncSession = None
    cls = None

    def __init__(self, db: AsyncSession, cls=None):
        self.db = db
        if cls is not None:
            # 如果实例化时不传递实体cls类型,则需要手动调用query(User)方法将模型cls传入
            self.cls = cls

    def query(self, cls):
        """
        设置查询模型
        """
        self.cls = cls
        return self

    def conditions(self, model: M):
        """
        组织查询过滤条件
        """
        filters = {}
        keys = model.__dict__.keys()
        values = model.__dict__.values()
        tmp = dict(zip(keys, values))
        for key, value in tmp.items():
            if value is not None and value != "" and key != "_sa_instance_state":
                filters[key] = value
        return filters

    async def execute_sql(self, sql, params) -> dict:
        """
        执行原始SQL
        """
        result_proxy = await self.db.execute(text(sql), params)
        row_proxy_list = result_proxy.fetchall()
        if not row_proxy_list:
            return None
        return [
            dict(zip(result_proxy.keys(), row_proxy)) for row_proxy in row_proxy_list
        ]

    # ===============================================business method====================================================

    async def save(self, model: M) -> M:
        """
        根据模型保存数据
        """
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def save_not_commit(self, model: M) -> M:
        """
        根据模型保存数据
        """
        self.db.add(model)
        return model

    async def save_all(self, models: list[M]) -> bool:
        """
        批量模型保存数据
        """
        self.db.add_all(models)
        await self.db.commit()
        return True

    async def save_all_not_commit(self, models: list[M]) -> bool:
        """
        批量模型保存数据
        """
        self.db.add_all(models)
        return True

    async def update(self, model: M) -> M:
        """
        根据模型更新数据
        """
        db_model = await self.db.merge(model)
        await self.db.commit()
        return db_model

    async def update_not_commit(self, model: M) -> M:
        """
        根据模型更新数据
        """
        db_model = await self.db.merge(model)
        return db_model

    async def update_all(self, models: list[M]) -> bool:
        """
        批量模型更新数据
        """
        for model in models:
            await self.update(model)
        return True

    async def update_all_not_commit(self, models: list[M]) -> bool:
        """
        批量模型更新数据
        """
        for model in models:
            await self.update_not_commit(model)
        return True

    async def delete(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        db_model = await self.find_by_id(model)
        if not db_model:
            return False
        await self.db.delete(db_model)
        await self.db.commit()
        return True

    async def delete_not_commit(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        db_model = await self.find_by_id(model)
        if not db_model:
            return False
        await self.db.delete(db_model)
        return True

    async def delete_by_id(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        db_model = await self.find_by_id(model)
        if not db_model:
            return False
        await self.db.delete(db_model)
        await self.db.commit()
        return True

    async def delete_by_id_not_commit(self, model: M) -> bool:
        """
        根据模型删除数据
        """
        db_model = await self.find_by_id(model)
        if not db_model:
            return False
        await self.db.delete(db_model)
        return True

    async def delete_all(self, models: list[M]):
        """
        批量根据模型删除数据
        """
        for model in models:
            await self.delete_by_id(model)
        return True

    async def delete_all_not_commit(self, models: list[M]):
        """
        批量根据模型删除数据
        """
        for model in models:
            await self.delete_by_id_not_commit(model)
        return True

    async def exists(self, model: M) -> bool:
        """
        根据模型查询判断数据是否存在
        """
        stmt = select(self.cls).filter_by(**self.conditions(model))
        result = await self.db.execute(stmt)
        return result.first() is not None

    async def count(self, model: M) -> int:
        """
        根据模型统计数据条数
        """
        stmt = select(self.cls).filter_by(**self.conditions(model))
        result = await self.db.execute(stmt)
        return len(result.all())

    async def find_by_id(self, model: M) -> M:
        """
        根据模型查询指定ID数据
        """
        stmt = select(self.cls).filter_by(id=model.id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def find_by_ids(self, ids: list[int], model: M = None) -> list[M]:
        """
        根据模型查询指定ID数据
        """
        if model is None:
            stmt = select(self.cls).filter(self.cls.id.in_(ids))
        else:
            stmt = (
                select(self.cls)
                .filter(self.cls.id.in_(ids))
                .filter_by(**self.conditions(model))
            )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def find_all(self, model: M, order: Order = None) -> list[M]:
        """
        根据模型查询所有数据,默认按id降序排序
        """
        stmt = select(self.cls).filter_by(**self.conditions(model))

        if order is not None:  # 如果提供了自定义排序,则使用自定义排序
            stmt = stmt.order_by(text(order.property + " " + order.direction))
        else:  # 否则,默认按id降序排序
            stmt = stmt.order_by(desc(self.cls.id))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def find_by(self, search: PageHelper[M]) -> Paginate:
        """
        根据模型查询分页数据
        """
        stmt = select(self.cls).filter_by(**self.conditions(search.query))
        if search.sorter and search.sorter.orders is not None:  # 组织排序
            for order in search.sorter.orders:
                stmt = stmt.order_by(text(order.property + " " + order.direction))

        result = await self.db.execute(stmt)

        # 创建分页对象
        if search.sorter and search.sorter.orders is not None:
            paginate = Paginate(
                result,
                search.pager.page_num,
                search.pager.page_size,
                search.sorter.orders,
            )
        else:
            paginate = Paginate(
                result, search.pager.page_num, search.pager.page_size, None
            )
        return paginate
