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
def list_users():
    """List users and show form to add user"""

    users = User.query.all()
    return render_template("list.html", users=users)


@app.post('/users/new')
def add_user():
    """Add user and redirect to user list"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form.get("image_url")

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.get('/<int:user_id>')
def show_user(user_id):
    """Display info on a single user"""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)


@app.get('/users/new')
def show_form():
    return render_template("new_user_form.html")
