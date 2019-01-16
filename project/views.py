#! /usr/bin/env python3
#
################
#
# project/views.py
#
################
#

"""
   Prepare a login and logout routes
"""

import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for

# config
app = Flask(__name__)
app.config.from_object("_config")

#
# Helper function
#


def connect_db():
    return sqlite3.connect(app.config["DATABASE_PATH"])


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for("login"))

    return wrap


#
# route handlers
#


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Goodbye!")
    return redirect(url_for("lgoin"))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form["username"] != app.config["USERNAME"]
            or request.form["password"] != app.config["PASSWORD"]
        ):
            error = "Invalid credentials. Please try again."
        return render_template("login.html", error=error)
    else:
        session["logged_in"] = True
        flash("Welcome!")
        return redirect(url_for("tasks"))
    return render_template("login.html")
