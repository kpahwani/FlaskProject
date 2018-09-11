"""
Module
"""
import os
from thermos import app, db, login_manager, mail
from flask import render_template, url_for, request, redirect, flash, session
from thermos.forms import BookmarkForm, LoginForm, RegisterForm, UploadFileForm, MailForm
from thermos.models import Bookmark, User
from werkzeug.utils import secure_filename
from flask_mail import Message
from flask_login import login_required, login_user, logout_user, current_user

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

bookmarks = []


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    Function
    """
    if current_user.is_authenticated:
        return render_template('index.html',
                               new_bookmarks=Bookmark.new_bookmarks(5),
                               upload_form=UploadFileForm(), mail_form=MailForm())
    else:
        return render_template('signup.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Function
    """
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(url=url, description=description, user_id=current_user.id)
        db.session.add(bm)
        db.session.commit()
        flash("Stored : {}".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def register():
    """
    Function
    """
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/signin', methods=['POST', 'GET'])
def login():
    """
    Function
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome {}'.format(user.username))
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash('Incorrect username/password')
    return render_template('signin.html', form=form)


def allowed_file(files):
    for file in files:
        if not ('.' in file.filename and
                file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
            return False
    return True


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    """
    Function
    """
    form = UploadFileForm()
    if form.validate_on_submit():
        files = request.files.getlist('uploaded_files')
        if files and allowed_file(files):
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Files uploaded successfully')
    return redirect(url_for('index'))


@app.route('/mail', methods=['GET', 'POST'])
def compose_mail():
    """
    Function
    :return: template
    """
    form = MailForm()
    if form.validate_on_submit():
        recipient = form.recipient.data
        subject = form.subject.data
        message = form.message.data
        msg = Message(recipients=[recipient],
                      subject=subject,
                      body=message,
                      sender=app.config['MAIL_USERNAME'])
        mail.send(msg)
        flash("Sent")
    return redirect(url_for('index'))


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/logout')
def logout():
    """
    Function
    """
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found_error(e):
    """
    Function
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """
    Function
    """
    return render_template('500.html'), 500
