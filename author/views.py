from flask_blog_c9 import app, db, uploaded_images
from flask import render_template, redirect, session, request, url_for, flash
from author.form import RegisterForm, LoginForm, EditAuthorForm
from author.models import Author
from blog.models import Post
from author.decorators import login_required, author_of_this, right_author
import bcrypt

POSTS_PER_PAGE = 5

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = Author.query.filter_by(
            username=form.username.data,
            ).first()
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                session['author_id'] = author.id
                flash("User %s logged in" % author.username)
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else:
                error = "Incorrect password"
        else:
            error = "Author profile not found"
    return render_template('author/login.html', form=form, error=error)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        
        image = request.files.get('image')
        filename = None
        try:
            filename = uploaded_images.save(image)
        except:
            flash("The image was not uploaded")
            
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            True,
            filename
        )
        db.session.add(author)
        db.session.commit()
        flash('Author profile sucessfully created')
        session['username'] = form.username.data
        session['is_author'] = author.is_author
        session['author_id'] = author.id
        return redirect(url_for('index'))
    return render_template('author/register.html', form=form, action='new')

@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_author')
    session.pop('author_id')
    flash("User logged out")
    return redirect(url_for('index'))

@app.route('/author_page/<int:author_id>')
def author_page(author_id, page=1):
    author = Author.query.filter_by(id = author_id).first_or_404()
    posts = Post.query.filter_by(author_id = author_id).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('author/author_page.html', author=author, posts=posts)

@app.route('/edit_author/<int:author_id>', methods=('GET', 'POST'))
@right_author
def edit_author(author_id):
    author = Author.query.filter_by(id=author_id).first_or_404()
    form = EditAuthorForm(obj=author)
    error = None
    
    print (form.fullname.data)
    
    if form.validate_on_submit():
        if bcrypt.hashpw(form.current_password.data, author.password) == author.password:
            original_image = author.image
            form.populate_obj(author)
            if form.image.has_file():
                image = request.files.get('image')
                try:
                    filename = uploaded_images.save(image)
                except:
                    flash("The image was not uploaded")
                if filename:
                    author.image = filename
            else:
                author.image = original_image
            
            if form.new_password.data:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(form.new_password.data, salt)
                author.password = hashed_password
    
            db.session.commit()
            flash('Author profile sucessfully updated')
            return redirect(url_for('index'))
        else:
            error = 'Incorrrect Password'
    return render_template('author/register.html', author=author,  form=form, error=error, action='edit')