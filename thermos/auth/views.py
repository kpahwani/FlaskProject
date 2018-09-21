"""
Module
"""
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user

from .. import db
from ..models import User
from . import auth
from .forms import LoginForm, RegisterForm


@auth.route('/signup', methods=['POST', 'GET'])
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


@auth.route('/signin', methods=['POST', 'GET'])
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
            return redirect(request.args.get('next') or url_for('user.user', username=user.username))
        flash('Incorrect username/password')
    return render_template('signin.html', form=form)


@auth.route('/logout')
def logout():
    """
    Function
    """
    logout_user()
    return redirect(url_for('main.index'))
