# !/usr/bin/python3
"""
功能描述
----------------------------------------------------
@Project :   now-find-agent
@File    :   FileUtil.py
@Contact :   zengxinmin@nowcoder.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/12/1 14:58   zengxinmin@nowcoder.com   1.0         None
"""
import os
import shutil

from loguru import logger


class FileUtil:
    """
    FileUtil是一个文件处理工具类,提供了常用的文件处理功能以及文件上传下载功能。
    """

    @staticmethod
    def create_file(file_path, content=None):
        """
        创建文件
        :param file_path: 文件路径
        :param content: 文件内容,默认为None
        :return: None
        """
        with open(file_path, "w") as f:
            if content:
                f.write(content)

    @staticmethod
    def read_file(file_path):
        """
        读取文件内容
        :param file_path: 文件路径
        :return: 文件内容
        """
        with open(file_path) as f:
            return f.read()

    @staticmethod
    def append_to_file(file_path, content):
        """
        在文件末尾追加内容
        :param file_path: 文件路径
        :param content: 追加的内容
        :return: None
        """
        with open(file_path, "a") as f:
            f.write(content)

    @staticmethod
    def copy_file(src_file_path, dst_file_path):
        """
        复制文件
        :param src_file_path: 源文件路径
        :param dst_file_path: 目标文件路径
        :return: None
        """
        shutil.copy(src_file_path, dst_file_path)

    @staticmethod
    def move_file(src_file_path, dst_file_path):
        """
        移动文件
        :param src_file_path: 源文件路径
        :param dst_file_path: 目标文件路径
        :return: None
        """
        shutil.move(src_file_path, dst_file_path)

    @staticmethod
    def delete_file(file_path):
        """
        删除文件
        :param file_path: 文件路径
        :return: None
        """
        os.remove(file_path)

    @staticmethod
    def cleanup_temp_file(file_path: str):
        """
        清理指定的临时文件

        Args:
            file_path: 要清理的文件路径
        """
        if file_path and os.path.exists(file_path):
            try:
                os.unlink(file_path)
                logger.info(f"已清理临时文件: {file_path}")

                # 尝试清理父目录(如果是空的)
                parent_dir = os.path.dirname(file_path)
                if parent_dir and os.path.exists(parent_dir):
                    try:
                        os.rmdir(parent_dir)
                        logger.info(f"已清理临时目录: {parent_dir}")
                    except OSError:
                        # 目录不为空,不需要删除
                        pass
            except Exception as e:
                logger.warning(f"清理临时文件失败: {e}")

    @staticmethod
    def cleanup_temp_paths(temp_paths: set):
        """
        清理指定的临时文件和目录集合

        Args:
            temp_paths: 要清理的临时路径集合
        """
        for temp_path in list(temp_paths):
            if os.path.exists(temp_path):
                try:
                    if os.path.isfile(temp_path):
                        os.unlink(temp_path)
                        logger.info(f"已清理临时文件: {temp_path}")
                    elif os.path.isdir(temp_path):
                        shutil.rmtree(temp_path)
                        logger.info(f"已清理临时目录: {temp_path}")
                except Exception as e:
                    logger.warning(f"清理临时路径失败 {temp_path}: {e}")
        temp_paths.clear()

    @staticmethod
    def cleanup_temp_directory(temp_dir: str):
        """
        清理指定的临时目录及其所有内容

        Args:
            temp_dir: 要清理的临时目录路径
        """
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"已清理临时目录: {temp_dir}")
            except Exception as e:
                logger.warning(f"清理临时目录失败: {e}")


if __name__ == "__main__":
    file_path = "test.txt"

    # 创建文件
    FileUtil.create_file(file_path, "Hello, FileUtil!")

    # 读取文件内容
    logger.info("文件内容:", FileUtil.read_file(file_path))

    # 在文件末尾追加内容
    FileUtil.append_to_file(file_path, "\nAppended text!")
    logger.info("文件内容:", FileUtil.read_file(file_path))

    # 复制文件
    copy_file_path = "copy_" + file_path
    FileUtil.copy_file(file_path, copy_file_path)

    # 移动文件
    move_file_path = "move_" + file_path
    FileUtil.move_file(copy_file_path, move_file_path)

    # 删除文件
    FileUtil.delete_file(file_path)
    FileUtil.delete_file(move_file_path)
