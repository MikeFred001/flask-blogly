"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect
from models import connect_db, db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def redirect_to_user_list():
    """Redirect to User List"""

    return redirect('/users')


@app.get('/users')
def list_users():
    """List users and show form to add user"""

    users = User.query.all()
    return render_template("list.html", users=users)


@app.get('/users/new')
def display_add_user_form():
    """Displays form to add a user"""

    return render_template("add_user_form.html")


@app.post('/users/new')
def add_user():
    """Add user and redirect to user list"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    image_url = request.form["image_url"]
    image_url = image_url if image_url else None

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
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
    return render_template("edit_user.html", user=user)


@app.post('/users/<int:user_id>/edit')
def process_edits(user_id):
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