from flask import Flask, url_for
import os
from os import path
from db import db
from db.models import users
from flask_login import LoginManager
from db.models_rgz import Employee, HRUser

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRT_KEY', 'vert-secret-key-12345')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ============== НАСТРОЙКА БАЗ ДАННЫХ ==============
if app.config['DB_TYPE'] == 'postgres':
    # Основная БД (для лабораторных работ)
    db_name = 'andrey_yanson_orm'
    db_user = 'andrey_yanson_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    # БД для РГЗ
    rgz_db_name = 'rgz_database'
    rgz_db_user = 'rgz_user'
    rgz_db_password = '123'

    # Настройка основной БД
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
    
    # Настройка дополнительной БД для РГЗ - ЭТО КЛЮЧЕВОЙ МОМЕНТ!
    app.config['SQLALCHEMY_BINDS'] = {
        'rgz': f'postgresql://{rgz_db_user}:{rgz_db_password}@{host_ip}:{host_port}/{rgz_db_name}'
    }
else:
    # Для SQLite
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "andrey_yanson_orm.db")
    rgz_db_path = path.join(dir_path, "rgz.db")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_BINDS'] = {
        'rgz': f'sqlite:///{rgz_db_path}'
    }

# Инициализация БД ПОСЛЕ настройки всех URI
db.init_app(app)

# Настройка LoginManager
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    # Пробуем загрузить из основной БД (лабораторные)
    user = users.query.get(int(login_id))
    if user:
        return user
    # Если нет, пробуем из БД РГЗ
    return HRUser.query.get(int(login_id))

# Регистрация blueprint'ов
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)

@app.route("/")
def index2():
    return '''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
        <head>
            <title> НГТУ, ФБ, Лабораторные работы </title>
        </head>
        <body>
            <header>
                НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
                <hr>
            </header>
            <main>
                <a href="/lab1">Первая лабораторная работа</a><br>
                <a href="/lab2/">Вторая лабораторная работа</a><br>
                <a href="/lab3/">Третья лабораторная работа</a><br>
                <a href="/lab4/">Четвертая лабораторная работа</a><br>
                <a href="/lab5/">Пятая лабораторная работа</a><br>
                <a href="/lab6/">Шестая лабораторная работа</a><br>
                <a href="/lab7/">Седьмая лабораторная работа</a><br>
                <a href="/lab8/">Восьмая лабораторная работа</a><br>
                <a href="/lab9/">Девятая лабораторная работа</a><br>
                <a href="/rgz/"><strong>Расчетно-графическое задание</strong></a>
            </main>
            <footer>
                <hr>
                &copy; Янсон Андрей, ФБИ-31, 3 курс, 2025 год
            </footer>
        </body>    
    </html>'''

@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="lab1/mistake.jpg")
    return f'''
         <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
        <head>
            <title> Лабораторная работа </title>
        </head>
        <body>
            <main>
                <h1> Такой страницы не существует!
                Вы явно что-то перепутали...
                </h1>
                <img src="{path}">
            </main>
            <footer>
                <hr>
                &copy; Янсон Андрей, ФБИ-21, 3 курс, 2024 год
            </footer>
        </body>    
    </html>
     ''', 404

@app.errorhandler(500)
def internal_error(err):
    path = url_for("static", filename="lab1/laugh.jpg")
    return f'''
    <!DOCTYPE html>
    <html>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
        <head>
            <title>Ошибка на сервере</title>
        </head>
        <body>
            <div>
                <h1>Произошла ошибка на сервере</h1>
                <img src="{path}">
                <p>К сожалению, при обработке вашего запроса возникла ошибка. Не вините себя, может когда-нибудь всё наладится...</p>
            </div>
        </body>
    </html>
    ''', 500

# Команды для инициализации БД
@app.cli.command("init-rgz-db")
def init_rgz_db():
    """Инициализация БД для РГЗ"""
    with app.app_context():
        # Создаем таблицы для bind 'rgz'
        db.create_all(bind=['rgz'])
        print("База данных РГЗ инициализирована")

@app.cli.command("add-hr-user")
def add_hr_user():
    """Добавление тестового пользователя-кадровика"""
    from werkzeug.security import generate_password_hash
    
    with app.app_context():
        # Проверяем, есть ли уже такой пользователь
        existing = HRUser.query.filter_by(username='hr_admin').first()
        if existing:
            print("Пользователь hr_admin уже существует")
            return
        
        # Создаем нового кадровика
        hr_user = HRUser(
            username='hr_admin',
            password=generate_password_hash('admin123'),
            full_name='Администратор Отдела Кадров'
        )
        db.session.add(hr_user)
        db.session.commit()
        print("Тестовый пользователь-кадровик создан:")
        print("Логин: hr_admin")
        print("Пароль: admin123")