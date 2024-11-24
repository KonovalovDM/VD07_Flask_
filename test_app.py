import unittest
from app import create_app, db, bcrypt
from app.models import User

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Настройка тестового клиента и тестовой базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем тестовую БД в памяти
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Очистка после теста"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def register_user(self, username, email, password):
        """Утилита для регистрации пользователя"""
        return self.client.post('/register', data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': password
        }, follow_redirects=True)

    def login_user(self, email, password):
        """Утилита для входа пользователя"""
        return self.client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        response = self.register_user('testuser', 'test@example.com', 'password123')
        self.assertIn('Вы успешно зарегистрировались'.encode('utf-8'), response.data)
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')

    def test_user_login(self):
        """Тест входа в систему"""
        self.register_user('testuser', 'test@example.com', 'password123')
        response = self.login_user('test@example.com', 'password123')
        self.assertIn('Добро пожаловать на домашнюю страницу'.encode('utf-8'), response.data)

    def test_profile_edit(self):
        """Тест редактирования профиля"""
        self.register_user('testuser', 'test@example.com', 'password123')
        self.login_user('test@example.com', 'password123')

        # Изменяем данные профиля
        response = self.client.post('/edit_profile', data={
            'username': 'updateduser',
            'email': 'updated@example.com',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123'
        }, follow_redirects=True)
        self.assertIn('Ваш профиль обновлен'.encode('utf-8'), response.data)

        # Проверяем изменения
        with self.app.app_context():
            user = User.query.filter_by(email='updated@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'updateduser')

    def test_duplicate_email_or_username(self):
        """Тест дублирующихся данных"""
        self.register_user('testuser', 'test@example.com', 'password123')
        self.register_user('duplicateuser', 'duplicate@example.com', 'password123')  # Зарегистрируем другого пользователя

        # Попытка изменить email на уже существующий
        self.login_user('duplicate@example.com', 'password123')
        response = self.client.post('/edit_profile', data={
            'username': 'duplicateuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn('Этот email уже используется.'.encode('utf-8'), response.data)

    def test_unauthorized_redirect(self):
        """Тест редиректов для неавторизованных пользователей"""
        response = self.client.get('/account', follow_redirects=True)
        self.assertIn('Пожалуйста, войдите для доступа к этой странице.'.encode('utf-8'), response.data)

        response = self.client.get('/edit_profile', follow_redirects=True)
        self.assertIn('Пожалуйста, войдите для доступа к этой странице.'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()
