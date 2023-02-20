import sqlite3
import sqlite3 as sq


def db_connect() -> None:
    global db, cur

    db = sq.connect('profiles.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS profiles(profile_id INTEGER PRIMARY KEY, from_email TEXT, password TEXT, to_email TEXT, subject TEXT)")

    db.commit()


def get_profiles() -> list:
    products = cur.execute("SELECT * FROM profiles").fetchall()
    return products


def create_new_profile(from_email, password, to_email, subject) -> sqlite3.Cursor:
    new_profile = cur.execute("INSERT INTO profiles (from_email, password, to_email, subject) VALUES (?, ?, ?, ?)",
                              (from_email,
                               password,
                               to_email,
                               subject))
    db.commit()

    return new_profile


def edit_profile(profile_id, from_email, password, to_email, subject) -> None:
    cur.execute(
        f"UPDATE profiles SET from_email = ?, password = password, to_email = to_email, subject = subject WHERE profile_id = ?",
        (from_email,
         password,
         to_email,
         subject,
         profile_id,))
    db.commit()
