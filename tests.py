# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy

from flask_blog_c9 import app, db

# need to add all models for db.create_all to work
from author.models import *
from blog.models import *

class UserTest(unittest.TestCase):
    def setUp(self):
        self.db_uri = 'mysql+pymysql://%s:%s@%s/' % (app.config['DB_USERNAME'], app.config['DB_PASSWORD'], app.config['DB_HOST'])
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['BLOG_DATABASE_NAME'] = 'test_blog'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("create database "  + app.config['BLOG_DATABASE_NAME'])
        db.create_all()
        conn.close()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("drop database "  + app.config['BLOG_DATABASE_NAME'])
        conn.close()

    def create_blog(self):
        return self.app.post('/setup', data=dict(
            name='My Test Blog',
            fullname='Clint Dunn',
            email='cdunn6754@yahoo.com',
            username='cdunn',
            password='test',
            confirm='test'
            ),
        follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def register_user(self, fullname, email, username, password, confirm):
        return self.app.post('/register', data=dict(
            fullname=fullname,
            email=email,
            username=username,
            password=password,
            confirm=confirm
            ),
        follow_redirects=True)

    def publish_post(self, title, body, category, new_category):
        return self.app.post('/post', data=dict(
            title=title,
            body=body,
            category=category,
            new_category=new_category,
            ),
        follow_redirects=True)
        
    def edit_author(self, author_id, fullname, email, username, password):
        return self.app.post('edit_author/%s' %author_id, 
        data=dict(current_password = password,
        fullname=fullname,
        email=email,
        username=username
        ),
        follow_redirects=True)
#######################################################################################################
    # Notice that our test functions begin with the word test;
    # this allows unittest to automatically identify the method as a test to run.
    def test_create_blog(self):
        rv = self.create_blog()
        assert 'Blog created' in str(rv.data)

    def test_login_logout(self):
        self.create_blog()
        rv = self.login('cdunn', 'test')
        assert 'User cdunn logged in' in str(rv.data)
        rv = self.logout()
        assert 'User logged out' in str(rv.data)
        rv = self.login('john', 'test')
        assert 'Author profile not found' in str(rv.data)
        rv = self.login('cdunn', 'wrong')
        assert 'Incorrect password' in str(rv.data)

    def test_user_creation(self):
        self.create_blog()
        self.login('cdunn', 'test')
        
        ## we dont have admin anymore
        #rv = self.app.get('/admin', follow_redirects=True)
        #assert 'Welcome, jorge' in str(rv.data)
        
        self.logout()
        rv = self.register_user('John Doe', 'john@example.com', 'john', 'test', 'test')
        assert 'Author profile sucessfully created' in str(rv.data)
        
        # registering will automatically login the user
        self.logout()
        
        rv = self.login('john', 'test')
        assert 'User john logged in' in str(rv.data)
        
        
    def test_posts_author_profile(self):
        self.create_blog()
        self.login('cdunn','test')
        
        rv = self.publish_post('hello this is the body test', 'Test Category', None, 'This is the test title')
        assert "Blog post created" in str(rv.data)
        
        self.logout()
        
        self.register_user('John Doe', 'john@example.com', 'john', 'test', 'test')
        
        self.login('john','test')
        
        # try to edit the first guys post
        rv = self.app.get('/edit_post/1', follow_redirects=True)
        assert "403 Forbidden" in str(rv.data)
        
        # now try to edit johns user profile with clint logged in
        self.logout()
        self.login('cdunn','test')
        rv = self.app.get('/edit_author/2', follow_redirects=True)
        assert "403 Forbidden" in str(rv.data)
        
        # now test that clint can edit his profile
        rv = self.edit_author(1,'Clint Dunn', 'cdunn6754@yahoo.com', 'cdunn', 'test')
        print(str(rv.data))
        assert 'Author profile sucessfully updated' in str(rv.data)
        
        
        

if __name__ == '__main__':
    unittest.main()