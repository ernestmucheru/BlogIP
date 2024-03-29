from flask import render_template,request,redirect,url_for,flash,abort
from . import main
from ..models import Post, User, Comment
from flask_login import login_required,current_user
from .forms import UpdateAccountForm,PostForm,CommentForm
from .. import db
from ..requests import getQuotes

import secrets
import os
from PIL import Image

@main.route("/home")
def home():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts)

@main.route('/')
def about():
    quote=getQuotes()
    return render_template('about.html', title = 'Quotes',quote=quote)

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



@main.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file, form=form)

@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form= PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('create_post.html' , title='New Post', form=form,  legend ='Update Post')

@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@main.route("/post/<int:post_id>/update",methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.post',post_id =post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post .content
    return render_template('create_post.html', title='Update Post', legend ='Update Post', form=form)

@main.route("/post/<int:post_id>/delete",methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@main.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())
    return render_template('user_posts.html', posts=posts, user=user)

@main.route('/comment',methods=['GET', 'POST'])
def comment():
    # post = Post.query.get_or_404(post_id)
    # content = Comment.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data
        form.content.data = ""
        new_comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
        db.session.add(new_comment)
        db.session.commit()
        # return redirect(url_for(main.home'))
        return redirect(url_for(".comment", id=post.id))

    return render_template('comments.html',title='New Comment',form=form , legend ='Add Comment')