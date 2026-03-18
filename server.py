from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB = "server.db"


def get_db():
    return sqlite3.connect(DB)


# ================= DATABASE =================
def init_db():

    conn = get_db()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password_hash TEXT,
        role TEXT,
        is_active INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS tests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_name TEXT,
        master_dictation TEXT,
        duration_sec INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT,
        test_id INTEGER,
        wpm INTEGER,
        accuracy INTEGER,
        errors INTEGER
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "Steno Sync Server Running"


# ================= USERS =================

# 🔥 CREATE USER (MOST IMPORTANT)
@app.route("/create_user", methods=["POST"])
def create_user():

    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO users (email,password_hash,role,is_active)
    VALUES (?,?,?,?)
    """,(
        data["email"],
        data["password_hash"],
        data["role"],
        data["is_active"]
    ))

    conn.commit()
    conn.close()

    return {"status": "user created"}


# GET USERS
@app.route("/get_users")
def get_users():

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT email,password_hash,role,is_active FROM users")
    rows = c.fetchall()

    users = []

    for r in rows:
        users.append({
            "email": r[0],
            "password_hash": r[1],
            "role": r[2],
            "is_active": r[3]
        })

    conn.close()

    return jsonify(users)


# ================= TESTS =================

@app.route("/tests")
def get_tests():

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT id,test_name,master_dictation,duration_sec FROM tests")
    rows = c.fetchall()

    tests = []

    for r in rows:
        tests.append({
            "id": r[0],
            "name": r[1],
            "dictation": r[2],
            "duration": r[3]
        })

    conn.close()
    return jsonify(tests)


# ================= RESULTS =================

@app.route("/upload_result", methods=["POST"])
def upload_result():

    data = request.json

    conn = get_db()
    c = conn.cursor()

    c.execute("""
    INSERT INTO results
    (name,roll_no,test_id,wpm,accuracy,errors)
    VALUES (?,?,?,?,?,?)
    """,(
        data["name"],
        data["roll_no"],
        data["test_id"],
        data["wpm"],
        data["accuracy"],
        data["errors"]
    ))

    conn.commit()
    conn.close()

    return {"status": "success"}


# ================= RUN =================

if __name__ == "__main__":

    init_db()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
