from enum import Enum

from pydantic import BaseModel, Field


class RobotState(str, Enum):
    """机器人运行状态。"""

    IDLE = "idle"
    RUNNING = "running"
    CHARGING = "charging"
    ERROR = "error"


class RobotCommand(str, Enum):
    """允许发送给机器人的指令。"""

    START = "start"
    STOP = "stop"
    RETURN_HOME = "return_home"


class Robot(BaseModel):
    """机器人状态数据。"""

    robot_id: str
    name: str
    online: bool
    battery: int = Field(ge=0, le=100)
    state: RobotState


class RobotCommandRequest(BaseModel):
    """客户端发送的机器人控制请求。"""

    command: RobotCommand


class RobotCommandResponse(BaseModel):
    """云端接受控制指令后的响应。"""

    robot_id: str
    command: RobotCommand
    accepted: bool
    message: str


class RobotStatusUpdate(BaseModel):
    """机器人上报的状态更新。"""

    online: bool | None = None
    battery: int | None = Field(default=None, ge=0, le=100)
    state: RobotState | None = None
