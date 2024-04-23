from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")