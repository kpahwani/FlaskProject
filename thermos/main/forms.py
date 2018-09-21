from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField, MultipleFileField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class UploadFileForm(Form):
    uploaded_files = MultipleFileField("Select: ")


class MailForm(Form):
    recipient = EmailField('To: ', validators=[DataRequired(), Email()])
    subject = StringField('Subject :')
    message = TextAreaField('Message: ')