from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TimeCreated:
    created_at = Column(
        DateTime, default=func.now(), index=True, nullable=False, comment="创建时间"
    )
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        index=True,
        nullable=False,
        comment="更新时间",
    )
    remark = Column(String(256), nullable=True, comment="备注")
