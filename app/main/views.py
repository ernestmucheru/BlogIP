from flask import render_template,url_for
from . import main
from ..models import posts



@main.route('/')
def home():
    return render_template('home.html', posts = posts)

@main.route('/about')
def about():
    return render_template('about.html', title = 'About')
