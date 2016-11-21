from flask_blog_c9 import db, uploaded_images

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80))
    email = db.Column(db.String(35), unique=True)
    username = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(60))
    is_author = db.Column(db.Boolean)
    image = db.Column(db.String(255))
    
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comment = db.relationship('Comment', backref='author', lazy='dynamic')
    
    @property
    def imgsrc(self):
        return uploaded_images.url(self.image)
    
    def __init__(self, fullname, email, username, password, is_author=False, image=None):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.is_author = is_author
        self.image = image

    def __repr__(self):
        return '<Author %r>' % self.username
