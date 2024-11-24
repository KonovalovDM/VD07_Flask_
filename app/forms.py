from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=35)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Passvord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует')


    def  validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Такая почта уже используется')

class LoginForm(FlaskForm):
     email = StringField('Email', validators=[DataRequired(), Email()])
     password = PasswordField('Password', validators=[DataRequired()])
     remember = BooleanField('Запомни меня')
     submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        Length(min=6),
        EqualTo('confirm_password', message='Пароли должны совпадать')
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Update Profile')

    def __init__(self, current_user, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.current_user = current_user

    def validate_username(self, username):
        if username.data != self.current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя уже занято.')

    def validate_email(self, email):
        if email.data != self.current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email уже используется.')
