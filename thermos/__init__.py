import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASEDIR, 'uploads/')

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xe38\x00m\xb0\xb7\xb1\x8b\xfbP\xc2\x98!W\xbe\x9cW\xe5\x14' \
                           '<\xba\xe2\xa6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR,
                                                                    'thermos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kaushal.pahwani@talentica.com'
app.config['MAIL_PASSWORD'] = '1@Jaishadaram'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
db = SQLAlchemy(app)


# login configuration
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

import thermos.views
import thermos.models
