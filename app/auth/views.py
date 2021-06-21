from flask import render_template,redirect,url_for,request,flash
from ..models import User
from .forms import RegistrationForm,LoginForm,UpdateAccountForm
from . import auth
from .. import db
from flask_login import login_user,login_required,logout_user,current_user


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
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            next_page = request.args.get('next')
            return redirect(request.args.get('next') or url_for('main.home'))
        else:
            flash('Invalid username or Password','danger')

    title = "Login"
    return render_template('auth/login.html',form = form,title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username =form.username.data
        current_user.email =form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'primary')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)