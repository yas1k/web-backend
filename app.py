from flask import Flask, url_for, redirect, request, abort, render_template
import datetime
import os

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

@app.route("/")
def index2():
    return '''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1.css">
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
            </main>
            <footer>
                <hr>
                &copy; Янсон Андрей, ФБИ-31, 3 курс, 2025 год
            </footer>
        </body>    
    </html>'''


@app.errorhandler(404)
def not_found(err):
    path = url_for("static", filename="mistake.jpg")
    return'''
         <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1.css">
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
    path = url_for("static", filename="laugh.jpg")
    return '''
    <!DOCTYPE html>
    <html>
    <link rel="stylesheet" href="/static/lab1.css">
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



