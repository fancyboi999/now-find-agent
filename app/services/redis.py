from typing import Any

from redis import StrictRedis

from config.config import get_settings

settings = get_settings()


class RedisService:
    """
    同步 Redis 数据库操作服务类

    当需要在同步环境中与Redis交互时,使用本类替代异步Redis客户端
    """

    @staticmethod
    def _get_connection() -> StrictRedis:
        """
        获取Redis数据库连接

        Returns:
            StrictRedis: Redis客户端连接
        """
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        db = settings.REDIS_DB
        password = settings.REDIS_PASSWORD

        if password:
            return StrictRedis(
                host=host, port=port, db=db, password=password, decode_responses=True
            )
        return StrictRedis(host=host, port=port, db=db, decode_responses=True)

    @classmethod
    def set_value(cls, key: str, value: Any, expire_seconds: int | None = None) -> None:
        """
        写入键值对

        Args:
            key: 键名
            value: 键值
            expire_seconds: 过期时间(秒),默认使用配置文件中的设置
        """
        expiration = (
            expire_seconds if expire_seconds is not None else settings.REDIS_EXPIRE
        )
        redis_client = cls._get_connection()
        redis_client.set(key, value, ex=expiration)

    @classmethod
    def get_value(cls, key: str) -> str | None:
        """
        读取键值

        Args:
            key: 键名

        Returns:
            Optional[str]: 键值,如果不存在则为None
        """
        redis_client = cls._get_connection()
        value = redis_client.get(key)
        return value

    @classmethod
    def hash_set(cls, hash_name: str, key: str, value: Any) -> None:
        """
        设置哈希表中的字段值

        Args:
            hash_name: 哈希表名
            key: 字段名
            value: 字段值
        """
        redis_client = cls._get_connection()
        redis_client.hset(hash_name, key, value)

    @classmethod
    def hash_multi_set(cls, hash_name: str, mapping: dict[str, Any]) -> None:
        """
        批量设置哈希表字段

        Args:
            hash_name: 哈希表名
            mapping: 包含键值对的字典
        """
        redis_client = cls._get_connection()
        redis_client.hmset(hash_name, mapping)

    @classmethod
    def hash_get(cls, hash_name: str, key: str) -> str | None:
        """
        获取哈希表中指定字段的值

        Args:
            hash_name: 哈希表名
            key: 字段名

        Returns:
            Optional[str]: 字段值,如果不存在则为None
        """
        redis_client = cls._get_connection()
        return redis_client.hget(hash_name, key)

    @classmethod
    def hash_get_all(cls, hash_name: str) -> dict[str, str]:
        """
        获取哈希表中所有字段和值

        Args:
            hash_name: 哈希表名

        Returns:
            Dict[str, str]: 哈希表中所有字段和值的字典
        """
        redis_client = cls._get_connection()
        return redis_client.hgetall(hash_name)

    @classmethod
    def delete(cls, *keys: str) -> None:
        """
        删除一个或多个键

        Args:
            keys: 要删除的键列表
        """
        redis_client = cls._get_connection()
        redis_client.delete(*keys)

    @classmethod
    def hash_delete(cls, hash_name: str, key: str) -> None:
        """
        从哈希表中删除指定字段

        Args:
            hash_name: 哈希表名
            key: 要删除的字段名
        """
        redis_client = cls._get_connection()
        redis_client.hdel(hash_name, key)

    @classmethod
    def set_expire(cls, key: str, expire_seconds: int | None = None) -> None:
        """
        设置键的过期时间

        注意:过期时间只能设置在顶级键上,不能为哈希表中的单个字段单独设置

        Args:
            key: 键名
            expire_seconds: 过期时间(秒),如果未提供则使用默认配置
        """
        expiration = (
            expire_seconds if expire_seconds is not None else settings.REDIS_EXPIRE
        )
        redis_client = cls._get_connection()
        redis_client.expire(key, expiration)
