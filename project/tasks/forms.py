#! /usr/bin/env python3
#
################
#
# project/tasks/forms.py
#
################
#

"""
    tasks application for the flask taskr.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    task_id = IntegerField()
    name = StringField("Task Name", validators=[DataRequired()])
    due_date = DateField(
        "Due Date (mm/dd/yyyy)", validators=[DataRequired()], format="%m/%d/%Y"
    )
    priority = SelectField(
        "Priority",
        validators=[DataRequired()],
        choices=[
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
        ],
    )
    status = IntegerField("Status")
