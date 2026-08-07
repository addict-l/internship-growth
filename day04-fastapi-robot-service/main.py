from fastapi import FastAPI, HTTPException, status

from models import (
    Robot,
    RobotCommandRequest,
    RobotCommandResponse,
    RobotStatusUpdate,
)
from robot_service import RobotService


app = FastAPI(
    title="Robot Cloud Service",
    description="学习用机器人云端接口模拟服务",
    version="0.1.0",
)

robot_service = RobotService()


@app.get("/health")
def health_check() -> dict[str, str]:
    """服务健康检查。"""
    return {"status": "ok"}


@app.get("/robots", response_model=list[Robot])
def list_robots() -> list[Robot]:
    """获取全部机器人。"""
    return robot_service.list_robots()


@app.get("/robots/{robot_id}", response_model=Robot)
def get_robot(robot_id: str) -> Robot:
    """获取指定机器人的状态。"""
    robot = robot_service.get_robot(robot_id)

    if robot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"没有找到机器人：{robot_id}",
        )

    return robot


@app.post(
    "/robots/{robot_id}/commands",
    response_model=RobotCommandResponse,
)
def send_robot_command(
    robot_id: str,
    request: RobotCommandRequest,
) -> RobotCommandResponse:
    """向指定机器人发送控制指令。"""
    robot = robot_service.get_robot(robot_id)

    if robot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"没有找到机器人：{robot_id}",
        )

    result = robot_service.send_command(
        robot_id,
        request.command,
    )

    if not result.accepted:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=result.message,
        )

    return result


@app.patch(
    "/robots/{robot_id}/status",
    response_model=Robot,
)
def update_robot_status(
    robot_id: str,
    update: RobotStatusUpdate,
) -> Robot:
    """模拟机器人上报运行状态。"""
    robot = robot_service.get_robot(robot_id)

    if robot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"没有找到机器人：{robot_id}",
        )

    return robot_service.update_status(robot_id, update)
