from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Required, Email
from ..models import User
from wtforms import ValidationError

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

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')