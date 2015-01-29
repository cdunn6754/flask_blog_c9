# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_blog import app
import sqlalchemy

try:
    db_uri = 'mysql://%s:%s@mysql:3306/' % (app.config['DB_USERNAME'], app.config['DB_PASSWORD'])
    engine = sqlalchemy.create_engine(db_uri)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute("create database "  + app.config['BLOG_DATABASE_NAME'])
    conn.close()
except:
    print "Database exists"

# Create tables for all models
from flask_blog import db
from user.models import *

db.create_all()