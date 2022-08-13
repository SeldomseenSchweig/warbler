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


class MessageModelTestCase(TestCase):
    """Test models for user."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_message_model(self):
        """Does basic message model work?"""

        u = User(
            email="test12@test.com",
            username="testuser12",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()



        m = Message(
            text="I am a message",
            user_id=u.id,
            
        )

        db.session.add(m)
        db.session.commit()



        self.assertIsInstance(m,Message)
        self.assertEqual(len(u.messages), 1)

    def test_message_model_for_message_count(self):
        """Does basic message model work?"""

        u = User(
            email="test9@test.com",
            username="testuser9",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()



        m = Message(
            text="I am a message",
            user_id=u.id,
            
        )

        db.session.add(m)
        db.session.commit()


        self.assertNotEqual(len(u.messages), 2)



    def test_message_model_for_message_user(self):
        """Checks if message has user id"""

        u = User(
            email="test22@test.com",
            username="testuser22",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()



        m = Message(
            text="I am a message",
            user_id=u.id,
            
        )

        db.session.add(m)
        db.session.commit()


        self.assertNotEqual(m.user_id,3)



    def test_message_likes(self):
        """"checks that message can be liked by user"""

        u1 = User(
            email="tes31@test.com",
            username="testuser3",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.commit()
        
        u2 = User(
            email="test4@test.com",
            username="testuser4",
            password="HASHED_PASSWORD"
        )

        db.session.add(u2)
        db.session.commit()

        m1 = Message(
            text="I am a message",
            user_id=u1.id,  
        )

        db.session.add(m1)
        db.session.commit()

        m2 = Message(
            text="I am a message",
            user_id=u2.id,  
        )

        db.session.add(m2)
        db.session.commit()

        u1.likes.append(m2)
        db.session.commit()

        u1.likes.append(m1)
        db.session.commit()
        
        self.assertEqual(len(u1.likes), 2)
        self.assertEqual(len(u2.likes), 0)
