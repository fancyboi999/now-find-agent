from asyncio import set_event_loop_policy

from uvloop import EventLoopPolicy

"""
用 uvloop 替换 asyncio 的默认事件循环, 提升性能
"""


set_event_loop_policy(EventLoopPolicy())
