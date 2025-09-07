from loguru import logger
from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import Pool

from config.config import get_settings

settings = get_settings()


# 从DATABASE_URL中提取schema信息
def extract_schema_from_url(database_url: str) -> str:
    """从数据库URL中提取schema名称

    优先从 URL 的 options 中的 search_path 提取；
    如未提供，则回退为使用数据库名作为 schema 名（与现有库一致的约定）。
    """
    import urllib.parse

    try:
        parsed = urllib.parse.urlparse(database_url)
        query_params = urllib.parse.parse_qs(parsed.query)

        # 处理 options=-c search_path=schema_name 格式
        if "options" in query_params:
            options = query_params["options"][0]
            if "search_path=" in options:
                schema = options.split("search_path=")[1].split(",")[0].strip()
                logger.info(f"从URL中提取到schema: {schema}")
                return schema

        # 回退：使用数据库名作为 schema 名
        db_name = parsed.path.lstrip("/") or "public"
        logger.info(f"从数据库名回退得到schema: {db_name}")
        return db_name
    except Exception as parse_error:
        logger.warning(f"解析DATABASE_URL获取schema失败，回退为public: {parse_error}")
        return "public"


# NOW Find Agent 数据库配置 - 如果未配置则使用SQLite
if not settings.DATABASE_URL:
    DATABASE_URL = "sqlite+aiosqlite:///./app.db"
    logger.info("DATABASE_URL未配置，使用默认的SQLite数据库")
else:
    DATABASE_URL = settings.DATABASE_URL
    logger.info(f"使用配置的数据库URL: {DATABASE_URL.split('@')[0].split('://')[-1] if '@' in DATABASE_URL else DATABASE_URL[:50]}...")  # 避免密码泄露


# TODO: 数据库连接事件监听器将在变量定义后设置


# 多数据库支持 - 智能检测和URL格式化
def detect_database_type(url: str) -> str:
    """检测数据库类型"""
    url_lower = url.lower()
    if any(db in url_lower for db in ["mysql", "mariadb"]):
        return "mysql"
    elif any(db in url_lower for db in ["postgresql", "postgres"]):
        return "postgresql"
    elif "sqlite" in url_lower:
        return "sqlite"
    else:
        return "unknown"

def format_database_url(url: str) -> str:
    """格式化数据库URL为正确的异步驱动格式"""
    if not url:
        return url
        
    db_type = detect_database_type(url)
    
    # 如果已经是正确的异步格式，直接返回
    if any(driver in url for driver in ["aiomysql", "asyncpg", "aiosqlite"]):
        return url
    
    # 根据数据库类型修正驱动
    if db_type == "mysql":
        if url.startswith("mysql://"):
            url = url.replace("mysql://", "mysql+aiomysql://", 1)
            logger.info("🔄 修正MySQL URL为异步驱动格式: mysql+aiomysql://")
        elif url.startswith("jdbc:mysql://"):
            # JDBC URL转换为SQLAlchemy格式
            jdbc_url = url.replace("jdbc:mysql://", "mysql+aiomysql://")
            # 简化参数，移除JDBC特有的参数
            import urllib.parse
            parsed = urllib.parse.urlparse(jdbc_url)
            query_params = urllib.parse.parse_qs(parsed.query)
            # 保留基本参数，移除JDBC特有参数
            safe_params = {k: v for k, v in query_params.items() 
                          if k not in ['statementInterceptors', 'useUnicode']}
            new_query = urllib.parse.urlencode(safe_params, doseq=True)
            url = urllib.parse.urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
            logger.info("🔄 转换JDBC MySQL URL为异步格式")
    elif db_type == "postgresql":
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            logger.info("🔄 修正PostgreSQL URL为异步驱动格式: postgresql+asyncpg://")
    elif db_type == "sqlite":
        if url.startswith("sqlite://"):
            url = url.replace("sqlite://", "sqlite+aiosqlite://", 1)
            logger.info("🔄 修正SQLite URL为异步驱动格式: sqlite+aiosqlite://")
    
    return url


# 获取格式化后的数据库URL
CLEANED_DATABASE_URL = format_database_url(DATABASE_URL)
DB_TYPE = detect_database_type(CLEANED_DATABASE_URL)

# 获取schema名称（使用清理后的URL）
SCHEMA_NAME = extract_schema_from_url(CLEANED_DATABASE_URL)

# 智能构建数据库连接参数
def build_connection_args(db_type: str, schema_name: str) -> dict:
    """根据数据库类型构建连接参数"""
    if db_type == "postgresql":
        return {
            "server_settings": {
                "application_name": "now-find-agent",
                "search_path": f"{schema_name},public",
            },
            "command_timeout": 60,
        }
    elif db_type == "mysql":
        return {
            "connect_timeout": 60,
            "autocommit": False,
        }
    elif db_type == "sqlite":
        return {
            "check_same_thread": False,  # SQLite异步需要
        }
    else:
        return {}

# 构建连接参数
ENGINE_CONNECT_ARGS = build_connection_args(DB_TYPE, SCHEMA_NAME)
logger.info(f"🔧 数据库类型: {DB_TYPE.upper()}, 连接参数已配置")

# 多数据库连接事件监听器设置
if DB_TYPE == "postgresql" and "asyncpg" not in CLEANED_DATABASE_URL:
    # 只对非asyncpg的PostgreSQL连接设置search_path
    @event.listens_for(Pool, "connect")
    def set_postgres_search_path(dbapi_connection, connection_record):
        """为PostgreSQL新连接设置search_path"""
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute(f"SET search_path TO {SCHEMA_NAME}, public")
            cursor.close()
            logger.debug(f"🔧 PostgreSQL连接设置search_path: {SCHEMA_NAME}")
        except Exception as e:
            logger.warning(f"⚠️ PostgreSQL设置search_path失败: {e}")
elif DB_TYPE == "mysql":
    # MySQL连接初始化（如果需要特殊设置）
    @event.listens_for(Pool, "connect")
    def set_mysql_settings(dbapi_connection, connection_record):
        """为MySQL连接设置特殊参数"""
        try:
            cursor = dbapi_connection.cursor()
            # 设置MySQL特定参数（如字符集、时区等）
            cursor.execute("SET NAMES utf8mb4")
            cursor.execute("SET time_zone = '+00:00'")
            cursor.close()
            logger.debug(f"🔧 MySQL连接初始化完成")
        except Exception as e:
            logger.warning(f"⚠️ MySQL连接初始化失败: {e}")
# SQLite不需要特殊的连接设置


""" 异步引擎

https://blog.csdn.net/meisanggou/article/details/104427146

pool_size
设置连接池中, 保持的连接数. 初始化时, 并不产生连接. 只有慢慢需要连接时, 才会产生连接. 例如我们的连接数设置成pool_size=10. 如果我们的并发量一直最高是5. 那么我们的连接池里的连接数也就是5. 当我们有一次并发量达到了10. 以后并发量虽然下去了, 连接池中也会保持10个连接.

max_overflow
当连接池里的连接数已达到, pool_size时, 且都被使用时. 又要求从连接池里获取连接时, max_overflow就是允许再新建的连接数.
例如pool_size=10, max_overflow=5. 当我们的并发量达到12时, 当第11个并发到来后, 就会去再建一个连接, 第12个同样. 当第11个连接处理完回收后, 若没有在等待进程获取连接, 这个连接将会被立即释放.

pool_timeout
从连接池里获取连接, 如果此时无空闲的连接. 且连接数已经到达了pool_size+max_overflow. 此时获取连接的进程会等待pool_timeout秒. 如果超过这个时间, 还没有获得将会抛出异常.
sqlalchemy默认30秒

pool_recycle
这个指, 一个数据库连接的生存时间. 例如pool_recycle=3600. 也就是当这个连接产生1小时后, 再获得这个连接时, 会丢弃这个连接, 重新创建一个新的连接.
当pool_recycle设置为-1时, 也就是连接池不会主动丢弃这个连接. 永久可用. 但是有可能数据库server设置了连接超时时间. 例如mysql, 设置的有wait_timeout默认为28800, 8小时. 当连接空闲8小时时会自动断开. 8小时后再用这个连接也会被重置.
"""
engine = create_async_engine(
    CLEANED_DATABASE_URL,  # 使用清理后的数据库URL
    echo=False,  # 是否打印出实际执行的 sql, 调试的时候可能更方便
    future=True,  # 使用 SQLAlchemy 2.0 API, 向后兼容
    max_overflow=15,  # 当连接池里的连接数已达到 pool_size 且都被使用时,
    pool_size=8,  # 接池中保持的连接数, 设置为 0 时表示连接无限制
    pool_recycle=60 * 15,  # 15 minutes, 设置时间以限制数据库自动断开
    pool_timeout=30.0,  # 如果超过这个时间, 还没有获得将会抛出异常
    pool_pre_ping=True,  # 启用连接预检查,在使用连接前先ping数据库
    pool_reset_on_return="commit",  # 连接返回池时重置状态
    connect_args=ENGINE_CONNECT_ARGS,
)
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # session.commit 之后仍然可以查询该对象
)


async def check_database_health():
    """多数据库健康检查 - 智能适配不同数据库类型"""
    try:
        async with async_session() as session:
            # 基本连接测试 - 所有数据库都支持
            await session.execute(text("SELECT 1"))
            
            # 根据数据库类型执行特定检查
            if DB_TYPE == "postgresql":
                # PostgreSQL特有检查
                result = await session.execute(text("SHOW search_path"))
                search_path = result.scalar()
                logger.debug(f"PostgreSQL search_path: {search_path}")
            elif DB_TYPE == "mysql":
                # MySQL特有检查
                result = await session.execute(text("SELECT DATABASE()"))
                db_name = result.scalar()
                logger.debug(f"MySQL当前数据库: {db_name}")
            elif DB_TYPE == "sqlite":
                # SQLite特有检查
                result = await session.execute(text("PRAGMA database_list"))
                db_info = result.fetchall()
                logger.debug(f"SQLite数据库列表: {len(db_info)} 个数据库")
            
        logger.info(f"✅ {DB_TYPE.upper()} 数据库健康检查通过")
        return True
    except Exception as e:
        logger.error(f"❌ {DB_TYPE.upper()} 数据库健康检查失败: {e}")
        return False


async def get_database_pool_status():
    """获取数据库连接池状态信息"""
    try:
        pool = engine.pool
        status = {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
        }

        # 尝试获取invalid状态,如果不存在则跳过
        try:
            status["invalid"] = pool.invalid()
        except AttributeError:
            # AsyncAdaptedQueuePool 没有 invalid() 方法
            logger.debug("连接池不支持invalid()方法,跳过该状态检查")

        return status
    except Exception as e:
        logger.error(f"获取连接池状态失败: {e}")
        return None
