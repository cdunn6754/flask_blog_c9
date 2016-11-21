from flask_wtf import Form
from wtforms import validators, StringField, PasswordField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import EmailField

class RegisterForm(Form):
    image = FileField('Image', validators=[
    FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    fullname = StringField('Full Name', [validators.Required()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('Current Password', [
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

class EditAuthorForm(Form):
    image = FileField('Image', validators=[
    FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    fullname = StringField('Full Name', [validators.Required()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    new_password = PasswordField('New Password', [
            validators.EqualTo('new_confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    new_confirm = PasswordField('Repeat Password')
    
    current_password = PasswordField('Current Password', [
        validators.Required(),
        validators.Length(min=4, max=80)
        ])
    