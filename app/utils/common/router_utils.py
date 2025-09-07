"""
工具函数,用于确定目标agent
"""


def determine_target_agent(user_input: str) -> str:
    """根据用户输入确定目标agent

    Args:
        user_input: 用户输入的文本

    Returns:
        目标agent的名称,如果没有匹配则返回None
    """
    # 精确指令到agent的映射
    exact_commands = {
        "字幕专家，帮我生成字幕": "subtitle_engineer",
        "封面专家，帮我生成封面": "cover_engineer",
        "视频专家，帮我合成视频": "video_engineer",
        "音频专家，帮我重新合成音频": "audio_engineer",
        "音频专家，帮我合成音频": "audio_engineer",
        # 可以添加更多精确指令
        "润色专家，帮我润色内容": "polisher",
    }

    # 检查是否完全匹配
    return exact_commands.get(user_input)
