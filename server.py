from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB = "server.db"

def get_db():
    return sqlite3.connect(DB)


@app.route("/")
def home():
    return "Steno Sync Server Running"


# GET USERS
@app.route("/users")
def get_users():
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT id,email,is_active,role FROM users")
    rows = c.fetchall()

    users = []
    for r in rows:
        users.append({
            "id": r[0],
            "email": r[1],
            "active": r[2],
            "role": r[3]
        })

    conn.close()
    return jsonify(users)


# GET TESTS
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


# UPLOAD RESULTS
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

    return {"status":"success"}


# GET USERS
@app.route("/get_users")
def get_users():

    conn = get_db()
    c = conn.cursor()

    c.execute("""
    SELECT email,password_hash,role,is_active
    FROM users
    """)

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


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
