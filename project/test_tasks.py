#! /usr/bin/env python3
#
################
#
# project/test.py
#
################
#

"""
    Unit Tests
"""

import unittest

from views import app, db
from models import User

TEST_DB = "test.db"


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

    def create_task(self):
        return self.app.post(
            "/add",
            data=dict(
                name="Go to the bank",
                due_date="01/30/2019",
                priority="1",
                posted_data="01/30/2019",
                status="1",
            ),
            follow_redirects=True,
        )

    def create_admin_user(self):
        new_user = User(
            name="root",
            email="admin@email.com",
            password="passwordOne",
            role="admin",
        )
        db.session.add(new_user)
        db.session.commit()

    #
    # Integration and Unit Tests
    #

    # each test should start with 'test'

    def test_users_can_add_tasks(self):
        self.create_user("newGuy", "newGuy@realpython.com", "passwordOne")
        self.login("newGuy", "passwordOne")
        response = self.create_task()
        self.assertIn(
            b"New entry was successfully posted. Thanks.", response.data
        )

    def test_users_connot_add_task_when_error(self):
        self.create_user("newGuy", "newGuy@realpython.com", "passwordOne")
        self.login("newGuy", "passwordOne")
        response = self.app.post(
            "/add",
            data=dict(
                name="Go to the Bank",
                due_date="",
                priority="1",
                posted_date="02/05/2019",
                status="1",
            ),
            follow_redirects=True,
        )
        self.assertIn(b"This field is required.", response.data)

    def test_users_can_complete_tasks(self):
        self.create_user("newGuy", "newGuy@realpython.com", "passwordOne")
        self.login("newGuy", "passwordOne")
        self.create_task()
        response = self.app.get("/complete/1", follow_redirects=True)
        self.assertIn(b"The task is complete. Nice.", response.data)

    def test_users_can_delete_tasks(self):
        self.create_user("newGuy", "newGuy@realpython.com", "passwordOne")
        self.login("newGuy", "passwordOne")
        self.create_task()
        response = self.app.get("/delete/1", follow_redirects=True)
        self.assertIn(b"The task was deleted.", response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user("newGuy", "newGuy@realpython.com", "passwordOne")
        self.login("newGuy", "passwordOne")
        self.create_task()
        self.logout()
        self.create_user("newGuy2", "newGuy2@realpython.com", "passwordOne")
        self.login("newGuy2", "passwordOne")
        response = self.app.get("/complete/1", follow_redirects=True)
        self.assertNotIn(b"The task is complete. Nice.", response.data)
        self.assertIn(
            b"You can only update tasks that belong to you.", response.data
        )

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user("newGuy", "newGuy@email.com", "passwordOne")
        self.login("newGuy", "passwordOne")
        # self.app.get("/tasks", follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user("newGuy2", "newGuy2@email.com", "passwordOne")
        self.login("newGuy2", "passwordOne")
        response = self.app.get("/delete/1", follow_redirects=True)
        self.assertIn(
            b"You can only delete tasks that belong to you.", response.data
        )


if __name__ == "__main__":
    unittest.main()
