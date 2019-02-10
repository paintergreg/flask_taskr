#! /usr/bin/env python3
#
################
#
# tests/test_main.py
#
################
#

"""
    Custom error pages.
"""

import unittest

from project import app, db
from project.models import User


class MainTests(unittest.TestCase):
    # Setup and Teardown

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.create_all()
        self.assertEquals(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Helper Methods
    def login(self, name, password):
        return self.app.post(
            "/", data=dict(name=name, password=password), follow_redirects=True
        )

    # tests
    def test_404_error(self):
        response = self.app.get("/not_a_route")
        self.assertEquals(response.status_code, 404)
        self.assertIn(b"Sorry. There\'s nothing here.", response.data)

    def test_500_error(self):
        bad_user = User(
            name="badUser", email="badUser@gmail.com", password="passwordOne"
        )
        db.session.add(bad_user)
        db.session.commit()
        self.assertRaises(ValueError, self.login, "badUser", "passwordOne")
        try:
            response = self.login("badUser", "passwordOne")
            self.assertEquals(response.status_code, 500)
            self.assertIn(b"Something went terribly wrong", response.data)
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
