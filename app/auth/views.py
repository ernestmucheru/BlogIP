from random import random
import secrets
import os
from flask import render_template,redirect,url_for,request,flash
from ..models import User,Post
from .forms import RegistrationForm,LoginForm,UpdateAccountForm,PostForm
from . import auth
from .. import db
from flask_login import login_user,login_required,logout_user,current_user
from PIL import Image
from flask_login import login_required



@auth.route("/")
@auth.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@auth.route('/about')
def about():
    return render_template('about.html', title = 'About')

@auth.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    title = "Sign Up"
    return render_template('auth/register.html', form = form)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            next_page = request.args.get('next')
            return redirect(request.args.get('next') or url_for('auth.home'))
        else:
            flash('Invalid username or Password','danger')

    title = "Login"
    return render_template('auth/login.html',form = form,title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.home"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join( 'app/static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file, form=form)

@auth.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form= PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('auth.home'))
    
    return render_template('create_post.html' , title='New Post',form=form)

@auth.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
