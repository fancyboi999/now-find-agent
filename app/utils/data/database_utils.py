"""
数据库更新工具类
用于统一处理数据库更新操作
"""

from typing import Any

from loguru import logger

from app.constants.workflow_constants import (ResultTypes, StateFields,
                                              TaskUpdateFields,
                                              UserUpdateFields,
                                              WorkUpdateFields)
from app.services.remote.task_service import TaskRemoteService
from app.services.remote.user_service import UserRemoteService
from app.services.remote.work_service import WorkRemoteService


class DatabaseUpdater:
    """数据库更新器类"""

    @staticmethod
    async def update_video_work(
        snapshot: Any, video_result_dict: dict[str, Any]
    ) -> None:
        """
        更新视频相关的work表

        Args:
            snapshot: 状态快照
            video_result_dict: 视频结果字典
        """
        work_service = WorkRemoteService(snapshot.values[StateFields.CORE_BASE_URL])
        await work_service.update_work_by_id(
            snapshot.values[StateFields.VIDEO_WORK_ID],
            {
                WorkUpdateFields.FILE_URL: video_result_dict["video_url"],
                WorkUpdateFields.PREVIEW_URL: video_result_dict["video_pic_url"],
                WorkUpdateFields.RESULT_TYPE: ResultTypes.VIDEO_SUCCESS,
                WorkUpdateFields.COST: video_result_dict["duration"],
            },
        )

    @staticmethod
    async def update_cover_work(
        snapshot: Any,
        cover_result_dict: dict[str, Any],
        final_result_flag: bool,
        final_cover_result_dict: dict[str, Any] | None = None,
    ) -> None:
        """
        更新封面相关的work表

        Args:
            snapshot: 状态快照
            cover_result_dict: 封面结果字典
            final_result_flag: 是否为最终结果
            final_cover_result_dict: 最终封面结果字典
        """
        work_service = WorkRemoteService(snapshot.values[StateFields.CORE_BASE_URL])

        if final_result_flag and final_cover_result_dict:
            await work_service.update_work_by_id(
                snapshot.values[StateFields.COVER_WORK_ID],
                {
                    WorkUpdateFields.FILE_URL: final_cover_result_dict[
                        "cover_video_url"
                    ],
                    WorkUpdateFields.PREVIEW_URL: final_cover_result_dict[
                        "cover_pic_url"
                    ],
                    WorkUpdateFields.RESULT_TYPE: ResultTypes.FINAL_SUCCESS,
                },
            )
        else:
            await work_service.update_work_by_id(
                snapshot.values[StateFields.COVER_WORK_ID],
                {
                    WorkUpdateFields.FILE_URL: cover_result_dict["cover_video_url"],
                    WorkUpdateFields.PREVIEW_URL: cover_result_dict["cover_pic_url"],
                    WorkUpdateFields.RESULT_TYPE: ResultTypes.COVER_PROCESSING,
                },
            )

    @staticmethod
    async def update_subtitle_work(
        snapshot: Any,
        subtitle_result_dict: dict[str, Any],
        final_result_flag: bool,
        final_subtitle_result_dict: dict[str, Any] | None = None,
    ) -> None:
        """
        更新字幕相关的work表

        Args:
            snapshot: 状态快照
            subtitle_result_dict: 字幕结果字典
            final_result_flag: 是否为最终结果
            final_subtitle_result_dict: 最终字幕结果字典
        """
        work_service = WorkRemoteService(snapshot.values[StateFields.CORE_BASE_URL])

        if final_result_flag and final_subtitle_result_dict:
            await work_service.update_work_by_id(
                snapshot.values[StateFields.SUBTITLE_WORK_ID],
                {
                    WorkUpdateFields.FILE_URL: final_subtitle_result_dict[
                        "subtitle_video_url"
                    ],
                    WorkUpdateFields.ASS_URL: final_subtitle_result_dict.get(
                        "subtitle_ass_url", ""
                    ),
                    WorkUpdateFields.PREVIEW_URL: final_subtitle_result_dict[
                        "subtitle_pic_url"
                    ],
                    WorkUpdateFields.RESULT_TYPE: ResultTypes.FINAL_SUCCESS,
                },
            )
        else:
            await work_service.update_work_by_id(
                snapshot.values[StateFields.SUBTITLE_WORK_ID],
                {
                    WorkUpdateFields.FILE_URL: subtitle_result_dict[
                        "subtitle_video_url"
                    ],
                    WorkUpdateFields.ASS_URL: subtitle_result_dict.get(
                        "subtitle_ass_url", ""
                    ),
                    WorkUpdateFields.PREVIEW_URL: subtitle_result_dict[
                        "subtitle_pic_url"
                    ],
                    WorkUpdateFields.RESULT_TYPE: ResultTypes.SUBTITLE_PROCESSING,
                },
            )

    @staticmethod
    async def update_user_points(snapshot: Any, points_to_deduct: Any | None) -> None:
        """
        更新用户积分

        Args:
            snapshot: 状态快照
            points_to_deduct: 要扣除的积分(如视频时长)
        """
        if points_to_deduct:
            user_service = UserRemoteService(snapshot.values[StateFields.CORE_BASE_URL])
            user_id = snapshot.values[StateFields.PID]
            await user_service.update_user_by_id(
                user_id, {UserUpdateFields.DEDUCT_POINTS: points_to_deduct}
            )
        else:
            logger.info("积分扣除条件不满足,跳过用户积分更新")

    @staticmethod
    async def update_task_progress(snapshot: Any, progress: Any) -> None:
        """
        更新任务进度

        Args:
            snapshot: 状态快照
            progress: 进度值
        """
        task_service = TaskRemoteService(snapshot.values[StateFields.CORE_BASE_URL])
        await task_service.update_task_by_id(
            str(snapshot.values[StateFields.TASK_ID]),
            {TaskUpdateFields.PROGRESS: progress},
        )
