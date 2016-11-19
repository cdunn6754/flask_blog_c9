from flask_blog_c9 import app
from flask import render_template, redirect, flash, url_for, session, request
from blog.form import SetupForm, PostForm, CommentForm
from flask_blog_c9 import db, uploaded_images
from author.models import Author
from blog.models import Blog, Post, Category, Comment
from author.decorators import login_required, author_required, author_of_post
import bcrypt
from slugify import slugify
from flask_uploads import UploadNotAllowed

POSTS_PER_PAGE = 5
COMMENTS_PER_PAGE = 5

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    blog = Blog.query.first()
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html', blog=blog, posts=posts)

@app.route('/admin')
@app.route('/admin/<int:page>')
@login_required
@author_required
def admin(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/admin.html', posts=posts)

@app.route('/setup', methods=('GET', 'POST'))
def setup():
    blogs = Blog.query.count()
    if blogs:
        return redirect(url_for('admin'))
    form = SetupForm()
    # grab the author that is currently logged in if there is one
    if session.get('username'):
        author = Author.query.filter_by(username = session.get('username')).first_or_404()
        form = SetupForm(obj=author)
        form.password.data = author.password
        form.confirm.data = author.password

    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author_new = Author(
        form.fullname.data,
        form.email.data,
        form.username.data,
        hashed_password,
        True)
        
        
        # if we arent signed in then just use the author that we just created
        if not session.get('username'):
            author = author_new
            db.session.add(author)
        # if the author was signed in but is_author = false change it becasuse
        # they are now
        author.is_author = True
        db.session.flush()
        if author.id:
            blog = Blog(form.name.data, author.id)
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()
            error = "Error creating user"
        if author.id and blog.id:
            db.session.commit()
        else:
            db.session.rollback()
            error = "Error creating blog"
        flash('Blog created')
        return redirect('/admin')
    return render_template('blog/setup.html', form=form)

@app.route('/post', methods=('GET', 'POST'))
#@author_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash("The image was not uploaded")
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        else:
            category = form.category.data
        blog = Blog.query.first()
        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        slug = slugify(title)
        post = Post(blog, author, title, body, category, filename, slug)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', slug=slug))
    return render_template('blog/post.html', form=form, action="new")
    
@app.route('/article/<slug>')
def article(slug, page=1):
    post = Post.query.filter_by(slug=slug).first_or_404()
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.publish_date.desc()).paginate(page, COMMENTS_PER_PAGE, False)
    print(len(comments.items))
    print ('HEREA       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return render_template('blog/article.html', post=post, comments=comments)
    
@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
@author_required
@author_of_post
def edit(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm(obj=post)
    if form.validate_on_submit():
        original_image = post.image
        form.populate_obj(post)
        if form.image.has_file():
            image = request.files.get('image')
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded")
            if filename:
                post.image = filename
        else:
            post.image = original_image
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category
        db.session.commit()
        return redirect(url_for('article', slug=post.slug))
    return render_template('blog/post.html', form=form, post=post, action="edit")

@app.route('/delete/<int:post_id>')
@author_required
def delete(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article deleted")
    return redirect('/admin')
    
@app.route('/<post_slug>/comment', methods=('GET', 'POST'))
#@author_required
def comment(post_slug):
    post = Post.query.filter_by(slug=post_slug).first_or_404() 
    form = CommentForm()
    if form.validate_on_submit():
        blog = Blog.query.first()
        author = Author.query.filter_by(username=session['username']).first_or_404()
        body = form.body.data
        comment = Comment(blog,author,post,body)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article', slug=post_slug))
    return render_template('blog/comment.html', form=form, post=post, action="new")
    

@app.route('/<post_slug>/edit_comment/<comment_id>', methods=('GET', 'POST'))
#@author_required
def edit_comment(post_slug,comment_id):
    post = Post.query.filter_by(slug=post_slug).first_or_404()
    comment = Comment.query.filter_by(id=comment_id).first_or_404()
    form = CommentForm(obj=comment)
    if form.validate_on_submit():
        comment.body = form.body.data
        db.session.commit()
        return redirect(url_for('article', slug=post_slug))
    return render_template('blog/comment.html', form=form, post=post, comment=comment, action="edi")