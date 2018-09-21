from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

from .config import config_by_name

# Instance initialisation
mail = Mail()
db = SQLAlchemy()

# login configuration
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# Moment
moment = Moment()

# Configure debug toolbar
toolbar = DebugToolbarExtension()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .bookmark import bookmark as bookmark_blueprint
    app.register_blueprint(bookmark_blueprint, url_prefix='/bookmark')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .user import user as user_auth
    app.register_blueprint(user_auth, url_prefix='/user')

    return app
