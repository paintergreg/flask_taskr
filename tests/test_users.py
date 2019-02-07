#! /usr/bin/env python3
#
################
#
# test_users.py
#
################
#

"""
  Unit tests for the user functions
"""

import unittest

from project import app, db
from project.models import User


class AllTests(unittest.TestCase):

    #
    # Setup and Teardown
    #

    # execute prior to each test
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        #     basedir, TEST_DB
        # )
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.create_all()

    # execute after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #
    # Helper functions
    #
    def login(self, name, password):
        return self.app.post(
            "/", data=dict(name=name, password=password), follow_redirects=True
        )

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post(
            "/register",
            data=dict(
                name=name, email=email, password=password, confirm=confirm
            ),
            follow_redirects=True,
        )

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    #
    # Integration and Unit Tests
    #

    # each test should start with 'test'
    def test_user_setup(self):
        self.create_user("newGuy", "newGuy@email.com", "passwordOne")
        test = db.session.query(User).all()
        for t in test:
            print(f"In test_user_setup :: {t}")
        self.assertEqual(t.name, "newGuy")
        self.assertEqual(t.email, "newGuy@email.com")
        self.assertEqual(t.password, "passwordOne")

    def test_form_is_present(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Please sign in to access your task list.", response.data
        )

    def test_users_cannot_login_unless_registered(self):
        response = self.login("foo", "bar")
        self.assertIn(b"Invalid username or password", response.data)

    def test_users_can_login(self):
        self.register(
            "newGuy", "newGuy@realpython.com", "passwordOne", "passwordOne"
        )
        response = self.login("newGuy", "passwordOne")
        self.assertIn(b"Welcome to FlaskTaskr", response.data)

    def test_invalid_form_data(self):
        self.register(
            "newGuy", "newGuy@realpython.com", "passwordOne", "passwordOne"
        )
        response = self.login("NotARegisteredUser", "NotAPassword")
        self.assertIn(b"Invalid username or password", response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Please register to access the task list.", response.data
        )

    def test_user_registration(self):
        self.app.get("/register", follow_redirects=True)
        response = self.register(
            "newGuy", "newGuy@realpython.com", "passwordOne", "passwordOne"
        )
        self.assertIn(b"Thanks for registering. Please login.", response.data)

    def test_user_registration_error(self):
        self.app.get("/register", follow_redirects=True)
        self.register(
            "newGuy", "newGuy@realpython.com", "passwordOne", "passwordOne"
        )
        self.app.get("/register", follow_redirects=True)
        response = self.register(
            "newGuy", "newGuy@realpython.com", "passwordOne", "passwordOne"
        )
        self.assertIn(
            b"That username and/or email already exist.", response.data
        )

    def test_logged_in_users_can_logout(self):
        self.register(
            "newGuy", "newGuy@realpython.com", "passwordOne", "passwordOne"
        )
        self.login("newGuy", "passwordOne")
        response = self.logout()
        self.assertIn(b"Goodbye!", response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b"Goodbye!", response.data)

    def test_logged_in_users_can_access_tasks_page(self):
        self.register(
            "newGuy", "newGuy@realpython.com", "passwordOne", "passwordOne"
        )
        self.login("newGuy", "passwordOne")
        response = self.app.get("/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add a new task:", response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get("/tasks", follow_redirects=True)
        self.assertIn(b"You need to login first.", response.data)

    def test_default_user_role(self):
        db.session.add(User("newGuy", "newGuy@realpython.com", "passwordOne"))
        db.session.commit()
        users = db.session.query(User).all()
        for user in users:
            self.assertEqual(user.role, "user")

    def test_task_template_displays_logged_in_user_name(self):
        self.register(
            "newGuy", "newGuy@realpython.com", "passwordOne", "passwordOne"
        )
        self.login("newGuy", "passwordOne")
        response = self.app.get("/tasks", follow_redirects=True)
        self.assertIn(b"newGuy", response.data)


if __name__ == "__main__":
    unittest.main()
