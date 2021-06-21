from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField,BooleanField,SubmitField
from wtforms import validators
from wtforms.validators import Required, Email,EqualTo
from ..models import User
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address', validators=[Required(),Email()])
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(),EqualTo('password_confirm',message = 'Password must match')])
    password_confirm = PasswordField('Confirm Passwords', validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError('Email already exists')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('Username is not available')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address', validators=[Required(),Email()])
    password = PasswordField('Password',validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
    email = StringField('Your Email Address', validators=[Required(),Email()])
    username = StringField('Enter your username',validators = [Required()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update Profile')

    def validate_email(self,email):
        if email.data != current_user.email:

            user= User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email already exists')

    def validate_username(self,username):
                user= User.query.filter_by(username = username.data).first()
                if user:
                    raise ValidationError('Username is not available')
