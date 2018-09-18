from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class RegisterForm(Form):
    username = StringField('Enter username', validators=[DataRequired()])
    password = PasswordField('Enter password', validators=[DataRequired()])
    email = StringField('Enter email', validators=[DataRequired(), Email()])


class LoginForm(Form):
    username = StringField('Enter username', validators=[DataRequired()])
    password = PasswordField('Enter password', validators=[DataRequired()])
