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
from forms import AddTaskForm
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

# config
app = Flask(__name__)
app.config.from_object("_config")
db = SQLAlchemy(app)

# This must follow the instantion of the SQLAlchemy class.SQLAlchemy
# The variable db is used in the models.py file.
from models import Task


#
# Helper function
#


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
    return redirect(url_for("login"))


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


@app.route("/tasks")
@login_required
def tasks():
    open_tasks = (
        db.session.query(Task).filter_by(status="1").order_by(Task.due_date.asc())
    )
    closed_tasks = (
        db.session.query(Task).filter_by(status="0").order_by(Task.due_date.asc())
    )
    return render_template(
        "tasks.html",
        form=AddTaskForm(request.form),
        open_tasks=open_tasks,
        closed_tasks=closed_tasks,
    )


@app.route("/add", methods=["GET", "POST"])
@login_required
def new_task():
    form = AddTaskForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            new_task = Task(form.name.data, form.due_date.data, form.priority.data, "1")
            db.session.add(new_task)
            db.session.commit()
            flash("New entry was successfully posted. Thanks.")
        return redirect(url_for("tasks"))


@app.route("/complete/<int:task_id>")
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({"status": "0"})
    db.session.commit()
    flash("The task is complete. Nice.")
    return redirect(url_for("tasks"))


@app.route("/delete/<int:task_id>")
@login_required
def delete_entry(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash("The task was deleted. Why not add a new one.")
    return redirect(url_for("tasks"))
