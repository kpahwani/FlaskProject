from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, PasswordField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Email, Regexp


class BookmarkForm(Form):
    url = URLField('The URL for your bookmark:', validators=[DataRequired(), url])
    description = StringField('Add an optional description:')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                                                  message='Tags can only contain letters and numbers')])


class RegisterForm(Form):
    username = StringField('Enter username', validators=[DataRequired()])
    password = PasswordField('Enter password', validators=[DataRequired()])
    email = StringField('Enter email', validators=[DataRequired(), Email()])