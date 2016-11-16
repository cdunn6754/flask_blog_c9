from functools import wraps
from flask import session, request, redirect, url_for, abort
from blog.models import Post

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_author') is False:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
   
def author_of_post(f):
    @wraps(f)
    def decorated_function(post_id):#*args, **kwargs):
        print(post_id)
        print(session.get('author_id'))
        post = Post.query.filter_by(id = post_id).first_or_404()
        if session.get('author_id') != post.author_id:
            abort(403)
        return f(post_id)#*args, **kwargs)
    return decorated_function    