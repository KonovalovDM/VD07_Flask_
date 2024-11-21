from flask import Flask
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User

class RegistratioForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])