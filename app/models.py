# from sqlalchemy.testing.pickleable import User

from app import db, login_manager
from flask_login import UserMixin # Этот класс дает возможность работать с пользователем

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # Эта строка будет отправлять в БД запрос для поиска определенного юзера по его ID

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self): # Функция, что бы представить информацию о пользователе в виде одной строчки
        return f'User: {self.username}, email: {self.email}'
