#! /usr/bin/env python3
#
################
#
# project/__init__.py
#
################
#

"""
docstring goes here.  be sure to write a good one ;)
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("_config.py")
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint

# register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
