import sqlite3
import logging
from threading import Lock

# name / path of highscore DB
DEFAULT_DB_PATH: str = "highscore.db"


class HighscoreDB:
    """singleton database class for managing the highscore with sqlite3 on one instance"""
    # class variable to store the single instance across all instances
    _instance = None
    # ensures single thread for DB connection
    _lock = Lock()

    def __new__(cls, db_pass: str = DEFAULT_DB_PATH):
        """calling __new__ special method (overriding __init__) to ensure only one instance is created"""
        with cls._lock:
            # create instance only if no one exists yet
            if cls._instance is None:
                # call parent class constructor with super() and default object creation method with __new__(cls)
                cls._instance = super().__new__(cls)
                cls._instance.db_pass = db_pass
                # trigger persisted connection to the DB; check_same_thread flag to allow multiple threads to sqlite db
                cls._instance._connection = sqlite3.connect(cls._instance.db_pass, check_same_thread=False)
                # init the db on the object
                cls._instance._init_db()
            return cls._instance

    def _init_db(self) -> None:
        """initializes the database and ensures the highscore table exists"""
        try:
            with self._connection as con:
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
        except sqlite3.Error as e:
            logging.error(f"Database initialization failed: {e}")

    def get_highscore(self) -> int:
        """reads the highscore from DB and returns it as int"""
        try:
            with self._connection as con:
                return con.execute("""
                    SELECT score FROM global_highscore
                    WHERE id = 1
                """).fetchone()[0]
        except sqlite3.Error as e:
            logging.error(f"Database reading failed: {e}")

    def update_highscore(self, new_highscore: int) -> None:
        """updates the highscore value in the db if delivered argument is higher than current DB value"""
        try:
            if new_highscore > self.get_highscore():
                with self._connection as con:
                    con.execute("""
                    UPDATE global_highscore SET score = ? WHERE id = 1
                    """, (new_highscore,))
        except sqlite3.Error as e:
            logging.error(f"Database writing failed: {e}")

    def close(self) -> None:
        """closes the database connection triggered by __del__ object destruction when app is terminated"""
        if hasattr(self, "_connection") and self._connection:
            self._connection.close()
            self._connection = None

    def __del__(self):
        """ensures database connection is closed on object destruction"""
        self.close()
