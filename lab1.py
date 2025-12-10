from flask import Blueprint, url_for, redirect, request
import datetime

lab1 = Blueprint('lab1', __name__)


@lab1.route("/index")
def index():
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
             <div class ="menu">
                <ol>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2/">Вторая лабораторная</a></li>
                </ol>
            </div>
        </main>
            <footer>
                <hr>
                &copy; Янсон Андрей, ФБИ-21, 3 курс, 2024 год
            </footer>
        </body>    
    </html>'''


@lab1.route("/lab1")
def lab_1():
    return '''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
        <head>
            <title> Лабораторная работа </title>
        </head>
        <body>
            <main>
                <p> Flask - фреймворк для создания веб-приложений на языке программирования
                Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
                Относится к категории так называемых микрофреймворков - минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <a href ="/">Корень сайта</a>
                <h2>Список роутов</h2>
                <a href ="/lab1/web">Сайт "web"</a>
                <a href ="/lab1/author">Сайт "author"</a>
                <a href ="/lab1/image">Сайт "oak"</a>
                <a href ="/lab1/counter">Сайт "counter"</a>
                <a href ="/lab1/info">Сайт "info"</a>
                <a href ="/lab1/created">Сайт "created"</a>
                <a href ="/lab1/erase">Сайт "erase"</a>
                <a href ="/lab1/400">Сайт "400"</a>
                <a href ="/lab1/401">Сайт "401"</a>
                <a href ="/lab1/402">Сайт "402"</a>
                <a href ="/lab1/403">Сайт "403"</a>
                <a href ="/lab1/405">Сайт "405"</a>
                <a href ="/lab1/418">Сайт "418"</a>
                <a href ="/lab1/error500">Сайт "error500"</a>
                <a href ="/lab1/custom">Сайт "custom"</a>

            </main>
            <footer>
                <hr>
                &copy; Янсон Андрей, ФБИ-21, 3 курс, 2024 год
            </footer>
        </body>    
    </html>
    '''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>\
        <html>\
        <link rel="stylesheet" href="/static/lab1/lab1.css">\
            <body>\
                <h1>web-сервер на flask</h1>\
                <a href="/lab1/author">author</a>\
                <a href="/lab1/oak">oak</a>\
                <a href="/lab1/counter">counter</a>\
                <a href="/lab1/created">created</a>\
            </body>\
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Янсон Андрей Алексеевич"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
        <link rel="stylesheet" href="/static/lab1/lab1.css">
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""


@lab1.route('/lab1/image')
def oak():
    path = url_for("static", filename="lab1/oak.jpg")
    css= url_for("static", filename ="lab1/lab1.css")
    return '''
    <!doctype html>
    <html>
        <link rel="stylesheet" href="/static/lab1/lab1.css">
        <body>
            
            <h1>Дуб</h1>
            <img src="''' + path +  '''">
            <a href="/lab1/web">web</a>
        </body>
    </html>
    ''', {
            'Content-language': 'ru'
        }

count = 0


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
        <body>
            Сколько раз мы сюда заходили: ''' + str(count) + '''
            <a href="/lab1/web">web</a>
            <a href="/lab1/erase">erase</a>
            <hr>
            Дата и время: ''' + str(time) + '''<br>
            Запрошенный адрес: ''' + url + '''<br>
            Ваш IP адресс: ''' + client_ip + '''<br>
        </body>
    </html>
    '''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return'''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
        <body>
            <h1> Создано успешно</h1>
            <div><i>что-то создано...</i></div>
            <a href="/lab1/web">web</a>
        </body>
    </html>
    ''', 201


@lab1.route("/lab1/erase")
def erase():
    global count
    count = 0
    return'''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1/lab1.css">
        <body>
            <h1>Счетчик обнулен</h1>
            <a href="/lab1/counter">counter</a>
        </body>
    </html>'''


@lab1.route("/lab1/400")
def fh():
    return'''
    сервер не понял, что от него хотят.
    ''', 400


@lab1.route("/lab1/401")
def fho():
    return'''
    Ошибка 401 выдается сервером в случае возникновения проблем
     с аутентификацией или авторизацией на сайте.
    ''', 401


@lab1.route("/lab1/402")
def fht():
    return'''
    это нестандартная ошибка клиента, зарезервированная для использования в будущем.
    ''', 402


@lab1.route("/lab1/403")
def fhth():
    return'''
    Ошибка 403 (Forbidden) — это когда сервер понял запрос,
     но почему-то отказывается выполнять его и отдавать браузеру HTML-код страницы.
    ''', 403


@lab1.route("/lab1/405")
def fhf():
    return'''
    Ошибки HTTP 405 возникают, когда метод HTTP не разрешен веб-сервером для запрошенного URL-адреса.
    ''', 405


@lab1.route("/lab1/418")
def fhei():
    return'''
    HTTP код ошибки 418 I'm a teapot сообщает о том,
    что сервер не может приготовить кофе, потому что он чайник.
    ''', 418


@lab1.route('/lab1/error500')
def trigger_error():
    return 1 / 0


@lab1.route('/lab1/custom')
def custom_route():
    path_to_img = url_for('static', filename='lab1/oak.jpg')
    return '''
<!DOCTYPE html>
<html>
<link rel="stylesheet" href="/static/lab1/lab1.css">
<head>
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>
<body>
    <div>
        <h1>7 причин почему рыбы хорошие друзья!</h1>
        <img src=''' + path_to_img + '''>
        <p>1.Рыбы оказывают на вас очень успокаивающее действие!</p>
        <p>2.Рыбы многофункциональные рассказчики.</p>
        <p>3.Рыбы не позволят вам доверять всему и всем</p>
        <h2>Я думал я перечисляю почему рыбки хорошие друзья, а оказалось в статье писали про знак зодиака... Поэтому я не буду перечислять дальше. Не верю в гороскопы
    </div>
</body>
</html>
    ''', 200, {
        'Content-Language': 'ru',
        'X-Custom-Header-1': '',
        'X-Custom-Header-2': ''
    }