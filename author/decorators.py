from functools import wraps
from flask import session, request, redirect, url_for, abort
from blog.models import Post
from author.models import Author

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
    
    
# this prevents the user from editing things  unless
# they should, an object is created of the model being edited is
# created from object_class and whatever id_member you would like that is a parameter to the
# decorated fucntion. This object needs to have an author_id member. The author_id of the
# object is compared to the session author_id to ensure only the author of the post/comment
# is able to edit it.

# e.g. for a edit_post
# object_class = Post (not a string)
# id_member = 'post_id' (string) (this is passed to post fcn anyways)

def author_of_this(object_class, id_member):
    def real_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            this_id = kwargs[str(id_member)]
            this_object = object_class.query.filter_by(id = this_id).first_or_404()
            if  not session['author_id'] == this_object.author_id:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return real_decorator
    
    
    
# very similar to author_of_this
# but for use with functions that are paramaterized with the author.id, rather 
# than a member of a generic object that has author_id as a member (that is what 
# author_of_this is used for)
def right_author(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        author_id = kwargs['author_id']
        author = Author.query.filter_by(id = author_id).first_or_404()
        if  not session['author_id'] == author.id:
            abort(403)
        return f(*args, **kwargs)
    return wrapper
