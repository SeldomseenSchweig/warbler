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


class UserViewTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample User. Add sample post"""

        User.query.delete()
        Message.query.delete()
        db.drop_all()
        db.create_all()

        user = User.signup(username='test1',email='test1@test.com',password='123456', image_url='https://cdn.pixabay.com/photo/2016/09/14/23/06/poznan-1670738__340.jpg')
        db.session.commit()

        message = Message(text="test_content", user_id = user.id)
        db.session.add(message)
        db.session.commit()

        self.User_id = user.id
        self.Post_id = message.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()




    def test_home(self):
            with app.test_client() as client:
                resp = client.get("/", follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn("<p>Sign up now to get your own personalized timeline!</p>", html)




    # def test_signup(self):

    #     with app.test_client() as client:
    #         d = {"username": "test2", "email": "test2@test.com",
    #             "password":'123456', "image_url":''}
    #         resp = client.post("/signup", data=d, follow_redirects=True)
    #         html = resp.get_data(as_text=True)

    #         self.assertEqual(resp.status_code, 200)



