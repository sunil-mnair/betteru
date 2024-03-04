from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired

username_required = "Please provide a username"
password_required = "Please provide a password"

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(message=username_required)])
    password = PasswordField('Password',validators=[InputRequired(message=password_required)])
    remember = BooleanField(False)

class SignupForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(message=username_required)])
    password = PasswordField('Password',validators=[InputRequired(message=password_required)])