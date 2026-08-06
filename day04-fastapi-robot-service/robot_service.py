from models import (
    Robot,
    RobotCommand,
    RobotCommandResponse,
    RobotState,
    RobotStatusUpdate,
)


class RobotService:
    """负责机器人数据和控制逻辑。"""

    def __init__(self) -> None:
        self.robots: dict[str, Robot] = {
            "robot-001": Robot(
                robot_id="robot-001",
                name="接待机器人一号",
                online=True,
                battery=86,
                state=RobotState.IDLE,
            ),
            "robot-002": Robot(
                robot_id="robot-002",
                name="巡检机器人二号",
                online=False,
                battery=42,
                state=RobotState.IDLE,
            ),
        }

    def list_robots(self) -> list[Robot]:
        """获取全部机器人。"""
        return list(self.robots.values())

    def get_robot(self, robot_id: str) -> Robot | None:
        """根据ID查询机器人。"""
        return self.robots.get(robot_id)

    def send_command(
        self,
        robot_id: str,
        command: RobotCommand,
    ) -> RobotCommandResponse:
        """模拟发送机器人控制指令。"""
        robot = self.get_robot(robot_id)

        if robot is None:
            raise ValueError("机器人不存在")

        if not robot.online:
            return RobotCommandResponse(
                robot_id=robot_id,
                command=command,
                accepted=False,
                message="机器人当前离线，无法执行指令。",
            )

        if command == RobotCommand.START:
            robot.state = RobotState.RUNNING
            message = "机器人已开始运行。"

        elif command == RobotCommand.STOP:
            robot.state = RobotState.IDLE
            message = "机器人已停止运行。"

        elif command == RobotCommand.RETURN_HOME:
            robot.state = RobotState.CHARGING
            message = "机器人正在返回充电点。"

        else:
            return RobotCommandResponse(
                robot_id=robot_id,
                command=command,
                accepted=False,
                message="暂不支持该指令。",
            )

        return RobotCommandResponse(
            robot_id=robot_id,
            command=command,
            accepted=True,
            message=message,
        )

    def update_status(
        self,
        robot_id: str,
        update: RobotStatusUpdate,
    ) -> Robot:
        """模拟机器人向云端上报状态。"""
        robot = self.get_robot(robot_id)

        if robot is None:
            raise ValueError("机器人不存在")

        if update.online is not None:
            robot.online = update.online

        if update.battery is not None:
            robot.battery = update.battery

        if update.state is not None:
            robot.state = update.state

        return robot
