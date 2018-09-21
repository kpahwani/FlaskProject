"""
Module
"""
from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_required, login_user, current_user

from .. import db
from ..models import Bookmark, User, Tag
from . import bookmark
from .forms import BookmarkForm, RegisterForm


@bookmark.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    Function
    """
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        tags = form.tags.data
        bm = Bookmark(url=url, description=description, user_id=current_user.id, tags=tags)
        db.session.add(bm)
        db.session.commit()
        flash("Stored : {}".format(description))
        return redirect(url_for('main.index'))
    return render_template('bookmark_form.html', form=form, title='Add bookmark')


@bookmark.route('/signup', methods=['POST', 'GET'])
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
        return redirect(url_for('main.index'))
    return render_template('signup.html', form=form)


@bookmark.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash('Updated {}'.format(bookmark.description))
        return redirect(url_for('user.user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title='Edit bookmark')


@bookmark.route('/delete/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    if request.method=='POST':
        db.session.delete(bookmark)
        db.session.commit()
        flash('Successfully deleted {}'.format(bookmark.description))
        return redirect(url_for('user.user', username=current_user.username))
    else:
        flash('Confirm deleting the bookmark')
    return render_template('confirm_delete.html', bookmark=bookmark, nolinks=True)


@bookmark.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)