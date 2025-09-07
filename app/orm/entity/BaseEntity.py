from app.core.db.DatabaseManager import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, func


class BaseEntity(Base):
    """
    实体基类(持久化模型由此类继承)
    """

    __abstract__ = True  ## 声明当前类为抽象类,被继承,调用不会被创建
    id = Column(Integer, primary_key=True, autoincrement=True)

    create_by = Column(String(64), comment="创建者")
    created_at = Column(
        TIMESTAMP, comment="创建时间", nullable=False, server_default=func.now()
    )
    update_by = Column(String(64), comment="更新者")
    updated_at = Column(
        TIMESTAMP,
        comment="更新时间",
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
