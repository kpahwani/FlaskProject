from flask import Blueprint

bookmark = Blueprint('bookmark', __name__)

from . import views
