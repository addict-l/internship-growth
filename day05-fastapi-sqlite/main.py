from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    HTTPException,
    Response,
    status,
)

from database import init_database
from models import (
    Robot,
    RobotCommandRequest,
    RobotCommandResponse,
    RobotCreate,
    RobotStatusUpdate,
)
from repository import DuplicateRobotError
from robot_service import (
    RobotConflictError,
    RobotNotFoundError,
    RobotService,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()

    yield


app = FastAPI(
    title="Robot Cloud Service",
    version="0.2.0",
    lifespan=lifespan,
)

robot_service = RobotService()

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "database": "sqlite",
    }

@app.get(
    "/robots",
    response_model=list[Robot],
)
def list_robots() -> list[Robot]:
    return robot_service.list_robots()

@app.get(
    "/robots",
    response_model=list[Robot],
)
def list_robots() -> list[Robot]:
    return robot_service.list_robots()

@app.post(
    "/robots",
    response_model=Robot,
    status_code=status.HTTP_201_CREATED,
)
def create_robot(
    robot: RobotCreate,
) -> Robot:

    try:
        return robot_service.create_robot(robot)

    except DuplicateRobotError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error

@app.patch(
    "/robots/{robot_id}/status",
    response_model=Robot,
)
def update_robot_status(
    robot_id: str,
    update: RobotStatusUpdate,
) -> Robot:

    try:
        return robot_service.update_status(
            robot_id,
            update,
        )

    except RobotNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

@app.delete(
    "/robots/{robot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_robot(
    robot_id: str,
) -> Response:

    try:
        robot_service.delete_robot(robot_id)

    except RobotNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )



@app.post(
    "/robots/{robot_id}/commands",
    response_model=RobotCommandResponse,
)
def send_robot_command(
    robot_id: str,
    request: RobotCommandRequest,
) -> RobotCommandResponse:

    try:
        return robot_service.send_command(
            robot_id,
            request.command,
        )

    except RobotNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except RobotConflictError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error