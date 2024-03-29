from flask import render_template,redirect,url_for,request,flash
from ..models import User
from .forms import RegistrationForm,LoginForm
from . import auth
from .. import db
from flask_login import login_user,login_required,logout_user,current_user
from flask_login import login_required
from ..email import mail_message


@auth.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to watchlist","email/welcome_user",user.email,user=user)
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

