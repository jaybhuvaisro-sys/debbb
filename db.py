import os
import pickle
import sqlite3
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_user_object(data):
    return pickle.loads(data)

def run_command(cmd):
    return subprocess.check_output(cmd, shell=True).decode()

def get_user(username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)
    return cur.fetchall()

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    path = os.path.join("uploads", f.filename)
    f.save(path)
    return jsonify({"status": "uploaded", "path": path})

@app.route("/deserialize", methods=["POST"])
def deserialize():
    data = request.data
    obj = load_user_object(data)
    return jsonify({"result": str(obj)})

@app.route("/exec", methods=["POST"])
def exec_cmd():
    cmd = request.json.get("cmd")
    output = run_command(cmd)
    return jsonify({"output": output})

@app.route("/user")
def user():
    username = request.args.get("username")
    result = get_user(username)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
