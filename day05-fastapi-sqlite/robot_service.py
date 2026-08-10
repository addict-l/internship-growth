from models import (
    Robot,
    RobotCommand,
    RobotCommandResponse,
    RobotCreate,
    RobotState,
    RobotStatusUpdate,
)
from repository import (
    DuplicateRobotError,
    RobotRepository,
)


class RobotNotFoundError(Exception):
    pass


class RobotConflictError(Exception):
    pass


class RobotService:

    def __init__(self) -> None:
        self.repository = RobotRepository()

    def list_robots(self) -> list[Robot]:
        return self.repository.list_robots()

    def get_robot(
        self,
        robot_id: str,
    ) -> Robot:

        robot = self.repository.get_robot(robot_id)

        if robot is None:
            raise RobotNotFoundError(
                f"没有找到机器人：{robot_id}"
            )

        return robot

    def create_robot(
        self,
        robot: RobotCreate,
    ) -> Robot:

        return self.repository.create_robot(robot)

    def update_status(
        self,
        robot_id: str,
        update: RobotStatusUpdate,
    ) -> Robot:

        robot = self.repository.update_status(
            robot_id,
            update,
        )

        if robot is None:
            raise RobotNotFoundError(
                f"没有找到机器人：{robot_id}"
            )

        return robot

    def delete_robot(
        self,
        robot_id: str,
    ) -> None:

        deleted = self.repository.delete_robot(
            robot_id
        )

        if not deleted:
            raise RobotNotFoundError(
                f"没有找到机器人：{robot_id}"
            )


    def send_command(
    self,
    robot_id: str,
    command: RobotCommand,
) -> RobotCommandResponse:

        robot = self.get_robot(robot_id)

        if not robot.online:
             raise RobotConflictError(
            "机器人当前离线，无法执行控制指令。"
          )

        if command == RobotCommand.START:
             new_state = RobotState.RUNNING
             message = "机器人已开始运行。"
        elif command == RobotCommand.STOP:
             new_state = RobotState.IDLE
             message = "机器人已停止运行。"
        elif command == RobotCommand.RETURN_HOME:
             new_state = RobotState.CHARGING
             message = "机器人正在返回充电点。"
        else:
             raise RobotConflictError(
                 f"不支持该机器人指令：{command}"
             )

        updated = self.repository.update_status(
        robot_id,
        RobotStatusUpdate(
            state=new_state,
        ),
    )

        if updated is None:
            raise RobotConflictError(
                f"更新机器人状态失败：{robot_id}"
            )

        return RobotCommandResponse(
        robot_id=robot_id,
        command=command,
        accepted=True,
        message=message,
    )