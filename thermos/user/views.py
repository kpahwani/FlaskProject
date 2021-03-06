"""
Module
"""

from flask import render_template

from ..models import User
from . import user


@user.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)
