import sqlite3
import sqlite3 as sq


def db_connect() -> None:
    global db, cur

    db = sq.connect('history.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY, date TEXT, CW EXT, HW TEXT)")

    db.commit()


def get_all_data() -> list:
    products = cur.execute("SELECT * FROM history").fetchall()
    return products


def create_new_data(date, cw, hw) -> sqlite3.Cursor:
    new_data = cur.execute("INSERT INTO history(date, CW, HW) VALUES (?, ?, ?)", (date, cw, hw))
    db.commit()
    return new_data