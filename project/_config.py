#! /usr/bin/env python3
#
################
#
# project/_config.py
#
################
#

"""
    Configuration file for the taskr project
"""

import os

# grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = "flasktaskr.db"
CSRF_ENABLED = True
SECRET_KEY = (
    "\xa5\x88\x8a\xa4\x04]\x9c\xfc-%\xb7\x90\x99\x96V1y\x98G\x93P\x95(\xb7"
)

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
