from flask import render_template
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<username>')
def user(username):
    return render_template('user.html', username=username)
