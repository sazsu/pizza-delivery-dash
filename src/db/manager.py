import os
import sqlite3
import time

# TODO: fetch and put game results in a db

# TODO: programmatically create db on startup


class Database:
    def __init__(self, name: str) -> None:
        db_path = self.get_path(name)
        self.conn = sqlite3.connect(db_path)
        self.on_startup()

    def on_startup(self) -> None:
        script_path = self.get_path('startup.sql')
        with open(script_path) as f:
            startup_script = f.read()
        with self.conn as conn:
            conn.executescript(startup_script)

    def get_stats(self) -> list[tuple[str, float]]:
        with self.conn as conn:
            results = conn.execute(
                """
                SELECT date, time_taken FROM Stats
                ORDER BY time_taken ASC
                """
            ).fetchall()
        return results

    def put_time(self, time_taken: float) -> None:
        current_date = time.strftime('%Y-%m-%d %I:%M:%S')
        with self.conn as conn:
            conn.execute(
                """
                INSERT INTO Stats (date, time_taken)
                VALUES(?, ?)
                """,
                (current_date, time_taken),
            )

    @staticmethod
    def get_path(name: str) -> str:
        return os.path.join(
            os.getcwd(),
            'src',
            'db',
            name,
        )
