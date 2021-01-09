#Imports related to forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

#Imports related to users
from flask_login import current_user
from talesBlogging.models import User

class RegistrationForm(FlaskForm):

    email = StringField("Email", validators = [DataRequired(), Email()])
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("passConfirm", message="Passwords don't match!")])
    passConfirm = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Sign up")

    def checkEmail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email address not available!")

    def checkUsername(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username not available!")

class UpdateUserForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    picture = FileField("Change profile picture", validators=[FileAllowed(["jpg", "png"])]) #Only jpg and png files allowed
    submit = SubmitField("Update")

    def checkEmail(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email address not available!")

    def checkUsername(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username not available!")

class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")
