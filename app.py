from flask import Flask, jsonify
import os, socket

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Hello from my K8s project",
                   version=os.getenv("APP_VERSION", "v1"),
                   pod=socket.gethostname())

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)app.py
