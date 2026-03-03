from flask import Flask, url_for, redirect, request, abort, render_template
import datetime
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager
from datetime import timedelta

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRT_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'andrey_yanson_orm'
    db_user = 'andrey_yanson_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "andrey_yanson_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

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
                <a href="/lab1">Первая лабораторная работа</a>
                <a href="/lab2/">Вторая лабораторная работа</a>
                <a href="/lab3/">Третья лабораторная работа</a>
                <a href="/lab4/">Четвертая лабораторная работа</a>
                <a href="/lab5/">Пятая лабораторная работа</a>
                <a href="/lab6/">Шестая лабораторная работа</a>
                <a href="/lab7/">Седьмая лабораторная работа</a>
                <a href="/lab8/">Восьмая лабораторная работа</a>
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
    return'''
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
                <img src="''' + path +  '''">
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
    return '''
    <!DOCTYPE html>
    <html>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
        <head>
            <title>Ошибка на сервере</title>
        </head>
        <body>
            <div>
                <h1>Произошла ошибка на сервере</h1>
                <img src="''' + path +  '''">
                <p>К сожалению, при обработке вашего запроса возникла ошибка. Не вините себя, может когда-нибудь всё наладится...</p>
            </div>
        </body>
    </html>
    ''', 500



