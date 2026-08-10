import sqlite3

from database import get_connection
from models import (
    Robot,
    RobotCreate,
    RobotStatusUpdate,
)


class DuplicateRobotError(Exception):
    """机器人ID已经存在。"""


class RobotRepository:
    """负责机器人数据库操作。"""

    @staticmethod
    def _row_to_robot(
        row: sqlite3.Row,
    ) -> Robot:
        return Robot(
            robot_id=row["robot_id"],
            name=row["name"],
            online=bool(row["online"]),
            battery=row["battery"],
            state=row["state"],
        )

    def list_robots(self) -> list[Robot]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT
                    robot_id,
                    name,
                    online,
                    battery,
                    state
                FROM robots
                ORDER BY robot_id
                """
            ).fetchall()

        return [
            self._row_to_robot(row)
            for row in rows
        ]

    def get_robot(
        self,
        robot_id: str,
    ) -> Robot | None:

        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT
                    robot_id,
                    name,
                    online,
                    battery,
                    state
                FROM robots
                WHERE robot_id = ?
                """,
                (robot_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_robot(row)

    def create_robot(
        self,
        robot: RobotCreate,
    ) -> Robot:

        try:
            with get_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO robots (
                        robot_id,
                        name,
                        online,
                        battery,
                        state
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        robot.robot_id,
                        robot.name,
                        int(robot.online),
                        robot.battery,
                        robot.state.value,
                    ),
                )

                connection.commit()

        except sqlite3.IntegrityError as error:
            raise DuplicateRobotError(
                f"机器人ID已存在：{robot.robot_id}"
            ) from error

        created = self.get_robot(robot.robot_id)

        if created is None:
            raise RuntimeError("创建机器人失败")

        return created

    def update_status(
        self,
        robot_id: str,
        update: RobotStatusUpdate,
    ) -> Robot | None:
        current = self.get_robot(robot_id)
        if current is None:
            return None

        online = (
            update.online
            if update.online is not None
            else current.online
        )
        battery = (
            update.battery
            if update.battery is not None
            else current.battery
        )
        state = (
            update.state
            if update.state is not None
            else current.state
        )

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE robots
                SET
                    online = ?,
                    battery = ?,
                    state = ?
                WHERE robot_id = ?
                """,
                (
                    int(online),
                    battery,
                    state.value,
                    robot_id,
                ),
            )
            connection.commit()

        return self.get_robot(robot_id)

        def delete_robot(
    self,
    robot_id: str,
) -> bool:

            with get_connection() as connection:
                rowcount = connection.execute(
                """
                DELETE FROM robots
                WHERE robot_id = ?
                """,
                (robot_id,),
            ).rowcount

            connection.commit()

            return rowcount > 0