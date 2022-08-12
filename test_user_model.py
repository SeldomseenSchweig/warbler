"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


db.create_all()


class UserModelTestCase(TestCase):
    """Test models for user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)



       

# Does the repr method work as expected?
    def test_repr_method(self):
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()



        self.assertEqual(repr(u), f'<User #{u.id}: {u.username}, {u.email}>')




# Does is_following successfully detect when user1 is following user2?
    def test_is_following(self):
        u1 = User(
            email="john316@dfmlkmv.com",
            username="u1",
            password="HASHED_PASSWORD"
        )
        db.session.add(u1)
        db.session.commit()

        u2 = User(
            email="test@test.com",
            username="u2",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()

        u1.following.append(u2)

        db.session.add(u1)
        db.session.commit()

        self.assertEqual(u1.is_following(u2), True)

        

    def test_is_not_following(self):
# Does is_following successfully detect when user1 is not following user2?
        u1 = User(
            email="john316@dfmlkmv.com",
            username="u3",
            password="HASHED_PASSWORD"
        )
        db.session.add(u1)
        db.session.commit()

        u2 = User(
            email="test@test.com",
            username="u4",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.is_following(u2), False)



# Does is_followed_by successfully detect when user1 is followed by user2?
    def test_is__followed_by(self):
        u1 = User(
            email="john316@dfmlkmv.com",
            username="u5",
            password="HASHED_PASSWORD"
        )
        db.session.add(u1)
        db.session.commit()

        u2 = User(
            email="test@test.com",
            username="u6",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()

        u1.following.append(u2)

        self.assertEqual(u2.is_followed_by(u1), True)

    def test_is_not_followed_by(self):
     # Does is_followed_by successfully detect when user1 is not followed by user2?

        u1 = User(
            email="john316@dfmlkmv.com",
            username="u7",
            password="HASHED_PASSWORD"
        )
        db.session.add(u1)
        db.session.commit()

        u2 = User(
            email="test@test.com",
            username="u8",
            password="HASHED_PASSWORD"
        )
        db.session.add(u2)
        db.session.commit()



        self.assertEqual(u2.is_followed_by(u1), False)




    def test_signup(self):
        """Does sign up model work?"""
        # Does User.create successfully create a new user given valid credentials?

        email="test@test.com",
        username="u9",
        password="HASHED_PASSWORD"
        image_url=''
        user = User.signup(username, email, password, image_url)

        self.assertIsInstance(user, User)

    def test_bad_signup(self):
        """Does sign up model work?"""
        # Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
        email="test@test.com",
        username="u10",
        password="HASHED_PASSWORD"
        image_url=''
        user1 = User.signup(username, email, password, image_url)
        db.session.commit()
        user2 = User.signup(username, email, password, image_url)

        self.assertRaises('sqlalchemy.exc.InvalidRequestError',db.session.commit())
    


# Does User.authenticate successfully return a user when given a valid username and password?
# Does User.authenticate fail to return a user when the username is invalid?
# Does User.authenticate fail to return a user when the password is invalid?
