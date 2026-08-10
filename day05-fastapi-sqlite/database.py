import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "robots.db"


def get_connection() -> sqlite3.Connection:
    """创建数据库连接。"""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def init_database() -> None:
    """初始化机器人数据库。"""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS robots (
                robot_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                online INTEGER NOT NULL,
                battery INTEGER NOT NULL
                    CHECK (battery >= 0 AND battery <= 100),
                state TEXT NOT NULL
            )
            """
        )

        connection.commit()