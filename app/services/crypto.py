from Crypto import Random
from Crypto.PublicKey import RSA
from loguru import logger

from config.config import get_settings

settings = get_settings()
"""所有加密解密功能已全部禁用
"""


def get_RAS_keys(name: str = "") -> None:
    """生成 RSA 密钥对.
        https://www.cnblogs.com/qxh-beijing2016/p/15249911.html

    需要生成 2 对 公钥私钥:
        前端: 公钥A + 私钥B: 公钥A 加密信息, 私钥B 签名
        后端: 私钥A + 公钥B: 私钥A 解密信息, 公钥B验证签名
    """
    rsa = RSA.generate(2048, Random.new().read)

    private_pem = rsa.exportKey()
    with open(f"private_{name}.pem", "wb") as f:
        f.write(private_pem)

    public_pem = rsa.publickey().exportKey()
    with open(f"public_{name}.pem", "wb") as f:
        f.write(public_pem)


def encrypt_data(data: str):
    """加密功能已禁用,直接返回原始数据"""
    logger.info("加密功能已禁用,返回原始数据")
    return data


def decrypt_data(data: str) -> str:
    """解密功能已禁用,直接返回原始数据"""
    logger.info("解密功能已禁用,返回原始数据")
    return data


def sign_data(data: str) -> str:
    """签名功能已禁用,直接返回原始数据"""
    logger.info("签名功能已禁用,返回原始数据")
    return data


def verifier_sign(data_decrypted: str, signature: str) -> bool:
    """验证签名功能已禁用,直接返回True"""
    logger.info("验证签名功能已禁用,直接返回True")
    return True


if __name__ == "__main__":
    get_RAS_keys("server")
    get_RAS_keys("client")
