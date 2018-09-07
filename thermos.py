"""
Module
"""
import os
from flask import Flask, render_template, url_for, request, redirect, flash, session
from forms import BookmarkForm, LoginForm, RegisterForm, UploadFileForm, MailForm

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


from flask_mail import Mail, Message

BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads/')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xe38\x00m\xb0\xb7\xb1\x8b\xfbP\xc2\x98!W\xbe\x9cW\xe5\x14' \
                           '<\xba\xe2\xa6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR,
                                                                    'thermos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kaushal.pahwani@talentica.com'
app.config['MAIL_PASSWORD'] = '1@Jaishadaram'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Import late as the db need to be initialised
import models


bookmarks = []


@app.route('/')
@app.route('/index')
def index():
    """
    Function
    """
    if session.get('user'):
        return render_template('index.html',
                               new_bookmarks=models.Bookmark.new_bookmarks(session['user'], 5),
                               upload_form=UploadFileForm(), mail_form=MailForm())
    else:
        flash('Login to continue')
        return render_template('signin.html', form=LoginForm())


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Function
    """
    form = BookmarkForm()
    if session.get('user') and form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = models.Bookmark(url=url, description=description, user_id=session['user'].get('id'))
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
        user = models.User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.to_json()
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/signin', methods=['POST', 'GET'])
def login():
    """
    Function
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        success, user = models.User.valid_user(username, password)
        if success:
            session['user'] = user.to_json()
            flash('Welcome {}'.format(user.username))
            return redirect(url_for('index'))
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


@app.route('/logout')
def logout():
    """
    Function
    """
    session.pop('user')
    flash('Successfully logged out')
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
