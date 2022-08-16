"""User view tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from app import CURR_USER_KEY, app, g
from models import db, User, Message, Follows, connect_db
from flask import session

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


# Now we can import app

from app import app
connect_db(app)



# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data




class UserViewTestCase(TestCase):
    """Tests for views for Users."""



    def register(self,username, email, password):
        return self.app.post(
            '/register',
            data=dict(username=username, email=email, password=password),
            follow_redirects=True
        )


    def setUp(self):
        """Add sample User. Add sample post"""

        app.config['WTF_CSRF_ENABLED'] = False
        db.drop_all()
        db.create_all()

        user1 = User.signup(username='test1',email='test1@test.com',password='123456', image_url='https://cdn.pixabay.com/photo/2016/09/14/23/06/poznan-1670738__340.jpg')
        db.session.commit()
        user2 = User.signup(username='test3',email='test3@test.com',password='123456', image_url='https://cdn.pixabay.com/photo/2016/09/14/23/06/poznan-1670738__340.jpg')
        db.session.commit()
        message = Message(text="test_content", user_id = user1.id)
        db.session.add(message)
        db.session.commit()
        user1.followers.append(user2)
        db.session.commit()



    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        
    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>Sign up now to get your own personalized timeline!</p>", html)


    def test_signup(self):
        """ Test for Handle signup form; add post and redirect to the user detail page."""
        with app.test_client() as client:
            d = {"username": "test2", "email":"test@content.com", "password":'123456', "image_url":''}
            resp = client.post("/signup", data=d, follow_redirects=True)

            html = resp.get_data(as_text=True)

            
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<p>@test2</p>", html)





    def test_signin(self):
        """ Test for Handle add form; add post and redirect to the user detail page."""
        with app.test_client() as client:
            form = {"username": "test1", "password":'123456'}
            resp = client.post("/login", data=form, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1", html)


    def test_show_following(self):
        """ When youre logged in, can you see the follower pages for any user?"""
        with app.test_client() as client:
                with client.session_transaction() as sess:
                    user = User.query.filter_by(username='test3').first()
                    sess[CURR_USER_KEY] = user.id
                resp = client.get(f"/users/{user.id}/following")
                html = resp.get_data(as_text=True)
                self.assertIn("<p>@test1</p>", html)
                self.assertEqual(resp.status_code, 200)

    def test_show_followers(self):
        """ When youre logged in, can you see the following pages for any user?"""
        with app.test_client() as client:
                with client.session_transaction() as sess:
                    user = User.query.filter_by(username='test1').first()
                    sess[CURR_USER_KEY] = user.id

                resp = client.get(f"/users/{user.id}/followers")
                html = resp.get_data(as_text=True)
                self.assertIn("<p>@test3</p>", html)
                self.assertEqual(resp.status_code, 200)


    def test_show_followers_not_logged_in(self):
        """ When youre logged out, are you disallowed from visiting a users follower / following pages??"""
        with app.test_client() as client:
                resp = client.get("/users/1/followers", follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn("Access unauthorized.", html)
                self.assertEqual(resp.status_code, 200)


    def test_add_message(self):
        """ When youre logged in, can you add a message as yourself?"""
        with app.test_client() as client:
                with client.session_transaction() as sess:
                    user = User.query.filter_by(username='test3').first()
                    sess[CURR_USER_KEY] = user.id
                
                print(sess[CURR_USER_KEY])
                form = {"text":"Blah blah blah"}
                resp = client.post('/messages/new', data=form, follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn("Blah blah blah", html)
                self.assertEqual(resp.status_code, 200)

    def test_delete_message(self):
        """ When youre logged in, can you delete a message as yourself?"""
        with app.test_client() as client:
                with client.session_transaction() as sess:
                    user = User.query.filter_by(username='test1').first()
                    sess[CURR_USER_KEY] = user.id
                    m = Message.query.filter_by(user_id=user.id).first()
                form = {"id":m.id}
                resp = client.post(f'/messages/{m.id}/delete', data=form, follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertNotIn("test_content", html)
                self.assertEqual(resp.status_code, 200)



    def test_delete_message_not_owned(self):
        """ When youre logged in, can you delete a message as you don't own?"""
        with app.test_client() as client:
                with client.session_transaction() as sess:
                    user = User.query.filter_by(username='test3').first()
                    sess[CURR_USER_KEY] = user.id
                    m = Message.query.filter_by(user_id=1).first()
                form = {"id":m.id}
                resp = client.post(f'/messages/{m.id}/delete', data=form, follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn("Access unauthorized", html)
                self.assertEqual(resp.status_code, 200)

    def test_delete_message_not_logged_in(self):
        """ When youre logged out, can you delete a message"""
        with app.test_client() as client:
                form = {"id":1}
                resp = client.post(f'/messages/1/delete', data=form, follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn("Access unauthorized", html)
                self.assertEqual(resp.status_code, 200)

    def test_add_message_not_logged_in(self):
        """ When youre logged out, can you add a message?"""
        with app.test_client() as client:
                form = {"text":"Blah blah blah"}
                resp = client.post('/messages/new', data=form, follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn("Access unauthorized", html)
                self.assertEqual(resp.status_code, 200)