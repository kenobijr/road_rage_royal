import sqlite3
import os
# name / path of highscore DB
DB_FILE: str = "highscore.db"


def init_db() -> None:
    """
    - on first running the game create and init a sqlite3 db to save the highscore
    - creates db and highscore table if not existing
    - highscore is global for all users on the instance
    - inserts default value for highscore
    """
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()
    # Create table with a constraint to enforce only one row
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_highscore (
        id INTEGER CHECK (id = 1),
        score INTEGER NOT NULL,
        PRIMARY KEY (id)
        )
    """)
    # check if row and therefore value exists already in the DB
    cursor.execute("""
        SELECT COUNT(*) FROM global_highscore
    """)
    if cursor.fetchone()[0] == 0:
        # insert initial value for highscore into DB only if empty yet
        cursor.execute("""
            INSERT INTO global_highscore (id, score)
            VALUES (?, ?)
        """, (1, 1))
        # commit it
        con.commit()
    # close db connection
    con.close()


def read_highscore() -> int:
    """reads the current highscore from DB and returns it as int"""
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()
    cursor.execute("""
        SELECT score FROM global_highscore
        WHERE id = 1
    """)
    highscore = cursor.fetchone()[0]
    con.close()
    return highscore


def update_highscore(new_highscore: int) -> None:
    """update the highscore in the DB"""
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()
    cursor.execute("""
        UPDATE global_highscore
        SET score = ?
        WHERE id = 1
    """, (new_highscore, ))
    con.commit()
    con.close()
