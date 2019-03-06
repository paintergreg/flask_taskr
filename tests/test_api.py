#! /usr/bin/env python3
#
################
#
# test/test_api.py
#
################
#

"""
docstring goes here.  be sure to write a good one ;)
"""


import unittest
from datetime import date

from project import app, db
from project.models import Task


class APITests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.create_all()
        self.assertEquals(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_tasks(self):
        db.session.add(
            Task(
                "Run around in circles",
                date(2015, 10, 22),
                10,
                date(2015, 10, 5),
                1,
                1,
            )
        )
        db.session.commit()

        db.session.add(
            Task(
                "Purchase Real Python",
                date(2016, 2, 23),
                10,
                date(2016, 2, 7),
                1,
                1,
            )
        )
        db.session.commit()

    def test_collection_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get("api/v1/tasks", follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, "application/json")
        self.assertIn(b"Run around in circles", response.data)
        self.assertIn(b"Purchase Real Python", response.data)

    def test_resource_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get("api/v1/tasks/2", follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, "application/json")
        self.assertIn(b"Purchase Real Python", response.data)
        self.assertNotIn(b"Run around in circles", response.data)

    def test_invalid_resource_endpoint_returns_error(self):
        self.add_tasks()
        response = self.app.get("/api/v1/tasks/209", follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.mimetype, "application/json")
        self.assertIn(b"Element does not exist", response.data)

if __name__ == "__main__":
    unittest.main()
