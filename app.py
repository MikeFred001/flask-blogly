"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect
from models import connect_db, db, User, Post
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Take-the-red-pill"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
debug = DebugToolbarExtension(app)

@app.get('/')
def redirect_to_user_list():
    """Redirect to User List"""

    return redirect('/users')


@app.get('/users')
def list_users():
    """List users and show form to add user"""

    users = User.query.order_by('first_name').all()

    return render_template("users_list.html", users=users)


@app.get('/users/new')
def display_add_user_form():
    """Displays form to add a user"""

    return render_template("add_user.html")


@app.post('/users/new')
def add_user():
    """Add user and redirect to user list"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    image_url = request.form["image_url"] or None

    user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.get('/users/<int:user_id>')
def show_user(user_id):
    """Display info on a single user"""

    user = User.query.get_or_404(user_id)
    return render_template("user_info.html", user=user)


@app.get('/users/<int:user_id>/edit')
def display_edit_form(user_id):
    """Display the form to edit a user's info"""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit_info.html", user=user)


@app.post('/users/<int:user_id>/edit')
def handle_edit_form(user_id):
    """Process edits on edit form and return user to users page"""

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.commit()

    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete's the user being displayed"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')




############################## User Post Routes ################################

@app.get('/users/<int:user_id>/posts/new')
def display_add_post_form(user_id):
    """Displays form to add post"""

    user = User.query.get_or_404(user_id)

    return render_template("user_add_post.html", user=user)


@app.post('/users/<int:user_id>/posts/new')
def handle_add_post_form(user_id):
    """Handle form to add a post"""
    user = User.query.get_or_404(user_id)

    new_post = Post(
        title=request.form['post_title'],
        content=request.form['post_content']
    )

    user.posts.append(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.get('/posts/<int:post_id>')
def display_post(post_id):
    """Displays a single post from a user"""

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template("user_post.html", post=post, user=user)


@app.get('/posts/<int:post_id>/edit')
def display_edit_post_form(post_id):
    """Displays form for user to edit post"""

    post = Post.query.get_or_404(post_id)

    return render_template("user_edit_post.html", post=post)


@app.post('/posts/<int:post_id>/edit')
def handle_edit_post_form(post_id):
    """Processes updates made by edit post form"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes currently displayed post"""

    post = Post.query.get_or_404(post_id)
    user = post.user

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')
