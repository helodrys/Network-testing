from flask import Flask, request, jsonify, render_template_string
import time
import random

app = Flask(__name__)

# Simple homepage
@app.route("/")
def home():
    return render_template_string("""
        <h1>Welcome to My Test Server</h1>
        <p>Try hitting <a href='/api/data'>/api/data</a> or POST to /login</p>
    """)

# Fake API that simulates DB delay
@app.route("/api/data")
def api_data():
    time.sleep(random.uniform(0.2, 0.8))  # simulate DB query delay
    return jsonify({
        "users": random.randint(100, 200),
        "status": "ok"
    })

# Fake login form (POST)
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    # simulate auth check
    time.sleep(random.uniform(0.1, 0.3))
    if username == "admin" and password == "123":
        return jsonify({"login": "success"})
    return jsonify({"login": "fail"}), 401

# A slow endpoint to simulate bottlenecks
@app.route("/slow")
def slow():
    time.sleep(random.uniform(1.0, 2.0))  # heavy computation
    return "This is a slow response!"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
