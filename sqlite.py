import sqlite3
import sqlite3 as sq


def db_connect() -> None:
    global db, cur

    db = sq.connect('data.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY, date TEXT, CW TEXT, HW TEXT)")

    cur.execute(
        "CREATE TABLE IF NOT EXISTS profiles(id INTEGER PRIMARY KEY, title TEXT, FROM_E_MAIL TEXT, PASS TEXT, TO_E_MAIL TEXT, SUBJECT TEXT)")

    db.commit()


def get_all_data() -> list:
    products = cur.execute("SELECT * FROM history").fetchall()
    return products


def create_new_data(date, cw, hw) -> sqlite3.Cursor:
    new_data = cur.execute("INSERT INTO history(date, CW, HW) VALUES (?, ?, ?)", (date, cw, hw))
    db.commit()
    return new_data


def get_profile(id) -> list:
    profile = cur.execute("SELECT * FROM profiles WHERE id = (?)", (id,)).fetchone()
    return profile


def create_new_profile(profile, title, FROM_E_MAIL, PASS, TO_E_MAIL, SUBJECT):
    existing_profile = get_profile(profile)

    if existing_profile:
        profile_id = existing_profile[0]
        new_profile = cur.execute(
            "UPDATE profiles SET title=?, FROM_E_MAIL=?, PASS=?, TO_E_MAIL=?, SUBJECT=? WHERE id=?",
            (title, FROM_E_MAIL, PASS, TO_E_MAIL, SUBJECT, profile_id)
        )
    else:
        new_profile = cur.execute(
            "INSERT INTO profiles(title, FROM_E_MAIL, PASS, TO_E_MAIL, SUBJECT) VALUES (?, ?, ?, ?, ?)",
            (title, FROM_E_MAIL, PASS, TO_E_MAIL, SUBJECT)
        )

    db.commit()
    return new_profile
