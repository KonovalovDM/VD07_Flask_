from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from app.models import User
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, EditProfileForm

# Создаем Blueprint
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались. Добро пожаловать!', 'success')
            return redirect(url_for('main.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Пользователь с таким именем или email уже существует.', 'danger')
        except ValueError:
            flash('Ошибка при хэшировании пароля. Попробуйте ещё раз.', 'danger')
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Введены неверные данные для входа.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.edit_profile'))  # Замените 'profile' на маршрут профиля
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)
