"""
工具类模块 - 提供各种实用工具函数和类
按功能分为以下几个子模块:
- core: 核心工具,如对象操作、序列化等
- common: 通用工具,如字符串处理、日期时间等
- io: IO相关工具,如文件操作、音频处理等
- web: Web相关工具,如HTTP请求、响应处理等
- data: 数据相关工具,如数据库操作、缓存等
- parsers: 解析相关工具,如JSON解析、事件处理等
"""

# 导入子模块
from app.utils import common, core, data, io, web
# 直接导出常用工具,方便使用
from app.utils.common.decorators import log_request
from app.utils.common.id_util import IdUtil
from app.utils.common.validate_util import V
from app.utils.core.object_dict import ObjectDict
from app.utils.core.object_util import ObjectUtil
from app.utils.web.resp_utils import R

__all__ = [
    "IdUtil",
    "ObjectDict",
    "ObjectUtil",
    "R",
    "V",
    "common",
    # 子模块
    "core",
    "data",
    "io",
    # 常用工具类直接导出
    "log_request",
    "web",
]
