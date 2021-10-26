from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from application.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(), Length(min=6, max=15)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(), Length(min = 6, max = 15)])
    password_confirm = PasswordField("Confirm Password", validators = [DataRequired(), Length(min = 6, max = 15),EqualTo("password")])
    first_name = StringField("First Name", validators = [DataRequired(),Length(min = 2, max = 55)])
    last_name = StringField("Last name", validators = [DataRequired(), Length(min = 2, max = 55)])
    submit = SubmitField("register Now")

    def validate_email(self, email):
        user = User.objects(email = email.data).first()
        if user:
            raise ValidationError("Email is already in use. Please use another one.")




