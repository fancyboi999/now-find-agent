from sqlalchemy import Boolean, Column, Integer, String

from .BaseModels import Base, TimeCreated


class Tool(Base, TimeCreated):
    __tablename__ = "tool"

    id = Column(
        Integer,
        unique=True,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        comment="llm id",
    )
    name = Column(String(256), nullable=False, comment="工具名称")
    description = Column(String(256), nullable=False, comment="工具描述")
    tool_function = Column(String(256), nullable=False, comment="工具对应程序函数")
    is_direct_return = Column(
        Boolean, nullable=False, default=False, comment="是否直接返回结果"
    )
    status = Column(Integer, nullable=False, comment="工具状态")
