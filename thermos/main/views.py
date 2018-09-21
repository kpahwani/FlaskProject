"""
Module
"""
import os

from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.utils import secure_filename

from ..models import Bookmark, User, Tag
from . import main
from .forms import UploadFileForm, MailForm
from .. import login_manager, mail
from ..config import UPLOAD_FOLDER, MAIL_USERNAME

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

bookmarks = []


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@main.route('/')
@main.route('/index')
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


def allowed_file(files):
    for file in files:
        if not ('.' in file.filename and
                file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
            return False
    return True


@main.route('/upload', methods=['POST', 'GET'])
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
                file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('Files uploaded successfully')
    return redirect(url_for('main.index'))


@main.route('/mail', methods=['GET', 'POST'])
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
                      sender=MAIL_USERNAME)
        mail.send(msg)
        flash("Sent")
    return redirect(url_for('main.index'))


@main.app_context_processor
def inject_tags():
    return dict(all_tags=Tag.all)


@main.app_errorhandler(404)
def page_not_found_error(e):
    """
    Function
    """
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    """
    Function
    """
    return render_template('500.html'), 500
