#!/usr/bin/env python3

import sqlite3
from flask import (Flask, render_template, g, flash, request, session, abort, redirect, url_for)

# settings
DATABASE = "/tmp/flaskr.db"
ENV = "development"
DEBUG = True
SECRET_KEY = "development key"
USERNAME = "admin"
PASSWORD = "default"

app = Flask(__name__)

app.config.from_object(__name__)


def db_conn():
    return sqlite3.connect(app.config["DATABASE"])


def init_db():
    with db_conn() as conn:
        with app.open_resource("schema.sql") as f:
            conn.cursor().executescript(f.read().decode())
        conn.commit()


@app.before_request
def before():
    g.conn = db_conn()


@app.teardown_request
def teardown(exception):
    g.conn.close()


@app.route('/')
def show_entries():
    cursor = g.conn.execute("SELECT title, text FROM entries ORDER BY id DESC")
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    return render_template("show_entries.html", entries=entries)


@app.route("/add", methods=["POST"])
def add_entry():
    if (not session.get("login")):
        abort(401)
    g.conn.execute("INSERT INTO entries (title, text) VALUES (?, ?)",
            [request.form.get("title"), request.form.get("text")])
    g.conn.commit()
    flash("New entry has been successfully posted")
    return redirect(url_for("show_entries"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if (request.method == "POST"):
        if (request.form.get("username") != app.config.get("USERNAME")):
            error = "Invalid username"
        elif (request.form.get("password") != app.config.get("PASSWORD")):
            error = "Invalid password"
        else:
            session["login"] = True
            flash("You're loginned successfully!")
            return redirect(url_for("show_entries"))
    return render_template("login.html", error=error)



@app.route("/logout")
def logout():
    session.pop("login", None)
    flash("You have logouted successfully!")
    return redirect(url_for("show_entries"))


if (__name__ == "__main__"):
    app.run()

