"""
通用常量定义
统一管理应用中使用的各种常量值
"""


class HTTPStatus:
    """HTTP状态码常量"""
    
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503


class ResponseMessage:
    """响应消息常量"""
    
    SUCCESS = "操作成功"
    CREATED = "创建成功"
    UPDATED = "更新成功"
    DELETED = "删除成功"
    
    # 错误消息
    BAD_REQUEST = "请求参数错误"
    UNAUTHORIZED = "未授权访问"
    FORBIDDEN = "禁止访问"
    NOT_FOUND = "资源不存在"
    CONFLICT = "资源冲突"
    INTERNAL_ERROR = "服务器内部错误"
    
    # 验证消息
    VALIDATION_ERROR = "数据验证失败"
    MISSING_FIELD = "缺少必填字段"
    INVALID_FORMAT = "数据格式不正确"


class CacheKeys:
    """缓存键常量"""
    
    USER_PREFIX = "user:"
    SESSION_PREFIX = "session:"
    TOKEN_PREFIX = "token:"
    
    # 缓存过期时间 (秒)
    DEFAULT_EXPIRE = 3600  # 1小时
    SHORT_EXPIRE = 300     # 5分钟
    LONG_EXPIRE = 86400    # 24小时


class DatabaseConstants:
    """数据库相关常量"""
    
    # 默认分页大小
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # 字符串长度限制
    SHORT_STRING_LENGTH = 50
    MEDIUM_STRING_LENGTH = 255
    LONG_STRING_LENGTH = 1000
    
    # 数据库操作超时 (秒)
    QUERY_TIMEOUT = 30


class Environment:
    """环境常量"""
    
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
    
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


class DateFormats:
    """日期格式常量"""
    
    DATE = "%Y-%m-%d"
    DATETIME = "%Y-%m-%d %H:%M:%S"
    ISO_DATETIME = "%Y-%m-%dT%H:%M:%SZ"
    TIMESTAMP = "%Y%m%d%H%M%S"


class RegexPatterns:
    """正则表达式模式"""
    
    EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    PHONE = r'^1[3-9]\d{9}$'  # 中国手机号
    PASSWORD = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{6,}$'  # 至少6位，包含字母和数字
    USERNAME = r'^[a-zA-Z0-9_]{3,20}$'  # 3-20位字母数字下划线
