import sqlite3
import os
# name / path of highscore DB
DB_FILE: str = "highscore.db"


class HighscoreDB:
    """singleton database class for managing the highscore with sqlite3 on one instance"""
    # class variable to store the single instance across all instances
    _instance = None

    def __new__(cls):
        """calling __new__ special method (overriding __init__) to ensure only one instance is created"""
        # create instance only if no one exists yet
        if cls._instance is None:
            # call parent class constructor with super() and default object creation method with __new__(cls)
            cls._instance = super().__new__(cls)
            # init the db on the object
            cls._instance._init_db()
        return cls._instance

    def _init_db(self) -> None:
        """initializes the database and ensures the highscore table exists"""
        with sqlite3.connect(DB_FILE) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS global_highscore (
                id INTEGER CHECK (id = 1),
                score INTEGER NOT NULL,
                PRIMARY KEY (id)
                )
            """)
            # only inserts the default value 1 if the row doesn't exist yet
            con.execute("""
                INSERT OR IGNORE INTO global_highscore (id, score) VALUES (1, 1)
            """)

    def read_db(self) -> int:
        """reads the highscore from DB and returns it as int"""
        with sqlite3.connect(DB_FILE) as con:
            return con.execute("""
                SELECT score FROM global_highscore
                WHERE id = 1
            """).fetchone()[0]

    def update_highscore(self, new_highscore: int) -> None:
        """updates the highscore value in the db with a new int argument"""
        with sqlite3.connect(DB_FILE) as con:
            con.execute("""
            UPDATE global_highscore SET score = ? WHERE id = 1
            """, (new_highscore,))
