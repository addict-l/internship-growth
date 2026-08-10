from enum import Enum

from pydantic import BaseModel, Field


class RobotState(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    CHARGING = "charging"
    ERROR = "error"


class RobotCommand(str, Enum):
    START = "start"
    STOP = "stop"
    RETURN_HOME = "return_home"


class RobotCreate(BaseModel):
    robot_id: str = Field(
        min_length=1,
        max_length=50,
    )

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    online: bool = True

    battery: int = Field(
        ge=0,
        le=100,
    )

    state: RobotState = RobotState.IDLE


class Robot(BaseModel):
    robot_id: str
    name: str
    online: bool
    battery: int
    state: RobotState


class RobotStatusUpdate(BaseModel):
    online: bool | None = None

    battery: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    state: RobotState | None = None


class RobotCommandRequest(BaseModel):
    command: RobotCommand


class RobotCommandResponse(BaseModel):
    robot_id: str
    command: RobotCommand
    accepted: bool
    message: str
