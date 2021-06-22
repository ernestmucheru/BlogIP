from flask import render_template
from . import main
from flask_login import login_required






@main.route('/')
@login_required
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html', title = 'About')
