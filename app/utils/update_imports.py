#!/usr/bin/env python3
"""
导入语句更新工具 - 用于更新代码中的导入语句以适应新的工具类结构
"""
import os
import re
from pathlib import Path

from loguru import logger

# 定义导入映射关系
IMPORT_MAPPINGS = {
    # 核心工具
    r"from app\.utils\.JsonUtil import": "from app.utils.core.json_util import",
    r"from app\.utils\.ReflectUtil import": "from app.utils.core.reflect_util import",
    r"from app\.utils\.object_util import": "from app.utils.core.object_util import",
    r"from app\.utils\.object_dict import": "from app.utils.core.object_dict import",
    r"from app\.utils\.serialization_utils import": "from app.utils.core.serialization_utils import",
    # IO工具
    r"from app\.utils\.FileUtil import": "from app.utils.io.file_util import",
    r"from app\.utils\.AudioUtil import": "from app.utils.io.audio_util import",
    r"from app\.utils\.OssUtil import": "from app.utils.io.oss_util import",
    # Web工具
    r"from app\.utils\.request_util import": "from app.utils.web.request_util import",
    r"from app\.utils\.NetUtils import": "from app.utils.web.net_utils import",
    r"from app\.utils\.RespUtils import": "from app.utils.web.resp_utils import",
    # 数据工具
    r"from app\.utils\.QueryUtil import": "from app.utils.data.query_util import",
    r"from app\.utils\.database_utils import": "from app.utils.data.database_utils import",
    r"from app\.utils\.RedisUtil import": "from app.utils.data.redis_util import",
    # 解析器工具
    r"from app\.utils\.CoorDiJsonUtils import": "from app.utils.parsers.coordinator_json_utils import",
    r"from app\.utils\.PlannerJsonUtils import": "from app.utils.parsers.planner_json_utils import",
    r"from app\.utils\.PolisherJsonUtils import": "from app.utils.parsers.polisher_json_utils import",
    r"from app\.utils\.TopicJsonUtils import": "from app.utils.parsers.topic_json_utils import",
    r"from app\.utils\.CheckEventUtils import": "from app.utils.parsers.check_event_utils import",
    r"from app\.utils\.WorkdataUtils import": "from app.utils.parsers.workdata_utils import",
    r"from app\.utils\.event_processor import": "from app.utils.parsers.event_processor import",
    r"from app\.utils\.node_processor import": "from app.utils.parsers.node_processor import",
    r"from app\.utils\.message_utils import": "from app.utils.parsers.message_utils import",
    r"from app\.utils\.parser_manager import": "from app.utils.parsers.parser_manager import",
    # 通用工具
    r"from app\.utils\.StrUtil import": "from app.utils.common.str_util import",
    r"from app\.utils\.DateUtil import": "from app.utils.common.date_util import",
    r"from app\.utils\.NumberUtil import": "from app.utils.common.number_util import",
    r"from app\.utils\.Md5Util import": "from app.utils.common.md5_util import",
    r"from app\.utils\.PathUtil import": "from app.utils.common.path_util import",
    r"from app\.utils\.ValidateUtil import": "from app.utils.common.validate_util import",
    r"from app\.utils\.id_util import": "from app.utils.common.id_util import",
    r"from app\.utils\.agent_utils import": "from app.utils.common.agent_utils import",
    r"from app\.utils\.RuntimeUtil import": "from app.utils.common.runtime_util import",
    r"from app\.utils\.SessionUtil import": "from app.utils.common.session_util import",
    r"from app\.utils\.function_analyzer import": "from app.utils.common.function_analyzer import",
    r"from app\.utils\.decorators import": "from app.utils.common.decorators import",
    # 简化导入
    r"import app\.utils\.FileUtil": "import app.utils.io.file_util",
    r"import app\.utils\.AudioUtil": "import app.utils.io.audio_util",
    r"import app\.utils\.OssUtil": "import app.utils.io.oss_util",
    r"import app\.utils\.JsonUtil": "import app.utils.core.json_util",
    r"import app\.utils\.ReflectUtil": "import app.utils.core.reflect_util",
    r"import app\.utils\.StrUtil": "import app.utils.common.str_util",
    r"import app\.utils\.DateUtil": "import app.utils.common.date_util",
    r"import app\.utils\.NumberUtil": "import app.utils.common.number_util",
    r"import app\.utils\.Md5Util": "import app.utils.common.md5_util",
    r"import app\.utils\.PathUtil": "import app.utils.common.path_util",
    r"import app\.utils\.ValidateUtil": "import app.utils.common.validate_util",
    r"import app\.utils\.NetUtils": "import app.utils.web.net_utils",
    r"import app\.utils\.RespUtils": "import app.utils.web.resp_utils",
    r"import app\.utils\.QueryUtil": "import app.utils.data.query_util",
    r"import app\.utils\.RedisUtil": "import app.utils.data.redis_util",
}

# 定义模块内导入映射关系
MODULE_IMPORT_MAPPINGS = {
    "app/utils/io/": {
        r"from app\.utils\.FileUtil import": "from .file_util import",
        r"from app\.utils\.AudioUtil import": "from .audio_util import",
        r"from app\.utils\.OssUtil import": "from .oss_util import",
    },
    "app/utils/core/": {
        r"from app\.utils\.JsonUtil import": "from .json_util import",
        r"from app\.utils\.ReflectUtil import": "from .reflect_util import",
        r"from app\.utils\.object_util import": "from .object_util import",
        r"from app\.utils\.object_dict import": "from .object_dict import",
        r"from app\.utils\.serialization_utils import": "from .serialization_utils import",
    },
    "app/utils/common/": {
        r"from app\.utils\.StrUtil import": "from .str_util import",
        r"from app\.utils\.DateUtil import": "from .date_util import",
        r"from app\.utils\.NumberUtil import": "from .number_util import",
        r"from app\.utils\.Md5Util import": "from .md5_util import",
        r"from app\.utils\.PathUtil import": "from .path_util import",
        r"from app\.utils\.ValidateUtil import": "from .validate_util import",
        r"from app\.utils\.id_util import": "from .id_util import",
        r"from app\.utils\.agent_utils import": "from .agent_utils import",
        r"from app\.utils\.RuntimeUtil import": "from .runtime_util import",
        r"from app\.utils\.SessionUtil import": "from .session_util import",
        r"from app\.utils\.function_analyzer import": "from .function_analyzer import",
        r"from app\.utils\.decorators import": "from .decorators import",
    },
    "app/utils/web/": {
        r"from app\.utils\.request_util import": "from .request_util import",
        r"from app\.utils\.NetUtils import": "from .net_utils import",
        r"from app\.utils\.RespUtils import": "from .resp_utils import",
    },
    "app/utils/data/": {
        r"from app\.utils\.QueryUtil import": "from .query_util import",
        r"from app\.utils\.database_utils import": "from .database_utils import",
        r"from app\.utils\.RedisUtil import": "from .redis_util import",
    },
    "app/utils/parsers/": {
        r"from app\.utils\.CoorDiJsonUtils import": "from .coordinator_json_utils import",
        r"from app\.utils\.PlannerJsonUtils import": "from .planner_json_utils import",
        r"from app\.utils\.PolisherJsonUtils import": "from .polisher_json_utils import",
        r"from app\.utils\.TopicJsonUtils import": "from .topic_json_utils import",
        r"from app\.utils\.CheckEventUtils import": "from .check_event_utils import",
        r"from app\.utils\.WorkdataUtils import": "from .workdata_utils import",
        r"from app\.utils\.event_processor import": "from .event_processor import",
        r"from app\.utils\.node_processor import": "from .node_processor import",
        r"from app\.utils\.message_utils import": "from .message_utils import",
        r"from app\.utils\.parser_manager import": "from .parser_manager import",
    },
}


def update_imports_in_file(file_path):
    """更新单个文件中的导入语句"""
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # 检查文件是否在某个模块内部
    module_path = None
    for module in MODULE_IMPORT_MAPPINGS:
        if module in file_path:
            module_path = module
            break

    # 如果是模块内部文件,使用相对导入
    if module_path:
        mappings = MODULE_IMPORT_MAPPINGS[module_path]
        for pattern, replacement in mappings.items():
            content = re.sub(pattern, replacement, content)
    else:
        # 否则使用全局导入映射
        for pattern, replacement in IMPORT_MAPPINGS.items():
            content = re.sub(pattern, replacement, content)

    # 如果内容有变化,写回文件
    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Updated imports in {file_path}")
        return True

    return False


def update_imports_in_directory(directory_path):
    """递归更新目录中所有Python文件的导入语句"""
    updated_files = 0

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if update_imports_in_file(file_path):
                    updated_files += 1

    return updated_files


if __name__ == "__main__":
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent

    # 更新app目录中的导入语句
    app_dir = project_root / "app"
    updated_count = update_imports_in_directory(app_dir)

    logger.info(f"Updated imports in {updated_count} files")
