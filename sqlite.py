import sqlite3


def db_connect():
    global db, cur

    db = sqlite3.connect('data.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS history_1(id INTEGER PRIMARY KEY, date TEXT, CW TEXT, HW TEXT)")

    cur.execute(
        "CREATE TABLE IF NOT EXISTS history_2(id INTEGER PRIMARY KEY, date TEXT, CW TEXT, HW TEXT)")

    cur.execute(
        "CREATE TABLE IF NOT EXISTS profiles(id INTEGER PRIMARY KEY, title TEXT, FROM_E_MAIL TEXT, PASS TEXT, TO_E_MAIL TEXT, SUBJECT TEXT)")

    db.commit()


def get_all_data(profile):
    if profile == 1:
        table = "history_1"
    else:
        table = "history_2"
    data = cur.execute("SELECT * FROM {}".format(table)).fetchall()
    return data


def create_new_data(profile, date, cw, hw):
    if profile == 1:
        table = "history_1"
    else:
        table = "history_2"
    new_data = cur.execute("INSERT INTO {}(date, CW, HW) VALUES (?, ?, ?)".format(table), (date, cw, hw))
    db.commit()
    return new_data


def get_profile(profile_id):
    profile = cur.execute("SELECT * FROM profiles WHERE id = ?", (profile_id,)).fetchone()
    return profile


def create_new_profile(profile_id, title, from_email, password, to_email, subject):
    existing_profile = get_profile(profile_id)

    if existing_profile:
        profile_id = existing_profile[0]
        new_profile = cur.execute(
            "UPDATE profiles SET title=?, FROM_E_MAIL=?, PASS=?, TO_E_MAIL=?, SUBJECT=? WHERE id=?",
            (title, from_email, password, to_email, subject, profile_id)
        )
    else:
        new_profile = cur.execute(
            "INSERT INTO profiles(title, FROM_E_MAIL, PASS, TO_E_MAIL, SUBJECT) VALUES (?, ?, ?, ?, ?)",
            (title, from_email, password, to_email, subject)
        )

    db.commit()
    return new_profile