import os

from flask import Flask, jsonify

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "dev")


@app.get("/")
def index():
    return jsonify(message="Hello from the pipeline demo", version=VERSION)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/greet/<name>")
def greet(name: str):
    return jsonify(greeting=f"Hello, {name}!")
