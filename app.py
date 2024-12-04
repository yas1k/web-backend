from flask import Flask, url_for, redirect, render_template
app = Flask(__name__)

@app.route("/index")
def index():
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
            </main>
            <footer>
                <hr>
                &copy; Янсон Андрей, ФБИ-21, 3 курс, 2024 год
            </footer>
        </body>    
    </html>'''

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
            </main>
            <footer>
                <hr>
                &copy; Янсон Андрей, ФБИ-21, 3 курс, 2024 год
            </footer>
        </body>    
    </html>'''

@app.route("/lab1")
def lab1():
    return '''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1.css">
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
                <a href ="/lab1/oak">Сайт "oak"</a>
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

@app.route("/lab1/web")
def web():
    return """<!doctype html>\
        <html>\
        <link rel="stylesheet" href="/static/lab1.css">\
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

@app.route("/lab1/author")
def author():
    name = "Янсон Андрей Алексеевич"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
        <link rel="stylesheet" href="/static/lab1.css">
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css= url_for("static", filename ="lab1.css")
    return '''
    <!doctype html>
    <html>
        <link rel="stylesheet" href="/static/lab1.css">
        <body>
            
            <h1>Дуб</h1>
            <img src="''' + path +  '''">
            <a href="/lab1/web">web</a>
        </body>
    </html>
    '''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1.css">
        <body>
            Сколько раз мы сюда заходили: ''' + str(count) + '''
            <a href="/lab1/web">web</a>
            <a href="/lab1/erase">erase</a>
        </body>
    </html>
    '''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return'''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1.css">
        <body>
            <h1> Создано успешно</h1>
            <div><i>что-то создано...</i></div>
            <a href="/lab1/web">web</a>
        </body>
    </html>
    ''', 201

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

@app.route("/lab1/erase")
def erase():
    global count
    count = 0
    return'''
    <!doctype html>
    <html>
    <link rel="stylesheet" href="/static/lab1.css">
        <body>
            <h1>Счетчик обнулен</h1>
            <a href="/lab1/counter">counter</a>
        </body>
    </html>'''

@app.route("/lab1/400")
def fh():
    return'''
    сервер не понял, что от него хотят.
    ''', 400

@app.route("/lab1/401")
def fho():
    return'''
    Ошибка 401 выдается сервером в случае возникновения проблем
     с аутентификацией или авторизацией на сайте.
    ''', 401

@app.route("/lab1/402")
def fht():
    return'''
    это нестандартная ошибка клиента, зарезервированная для использования в будущем.
    ''', 402

@app.route("/lab1/403")
def fhth():
    return'''
    Ошибка 403 (Forbidden) — это когда сервер понял запрос,
     но почему-то отказывается выполнять его и отдавать браузеру HTML-код страницы.
    ''', 403

@app.route("/lab1/405")
def fhf():
    return'''
    Ошибки HTTP 405 возникают, когда метод HTTP не разрешен веб-сервером для запрошенного URL-адреса.
    ''', 405

@app.route("/lab1/418")
def fhei():
    return'''
    HTTP код ошибки 418 I'm a teapot сообщает о том,
    что сервер не может приготовить кофе, потому что он чайник.
    ''', 418

@app.route('/lab1/error500')
def trigger_error():
    return 1 / 0

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

@app.route('/lab1/custom')
def custom_route():
    path_to_img = url_for('static', filename='oak.jpg')
    return '''
<!DOCTYPE html>
<html>
<link rel="stylesheet" href="/static/lab1.css">
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

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "Такого цветка нет", 404
    else:
        return f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Информация о цветке</title>
                <link rel="stylesheet" href="/static/lab1/lab1.css">
            </head>
            <body>
                <h1>Информация о цветке</h1>
                <h2>Цветок: {flower_list[flower_id]} - отличный выбор!</h2>
                <p>Идентификатор: {flower_id}</p>
                <a href="/lab2/all_flowers">Посмотреть все цветы</a><br>
                <a href="/lab2/add_flower/">Добавить новый цветок</a>
            </body>
        </html>
        '''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1> Добавлен новый цветок </h1>
    <p> Название нового цветка: {name} </p>
    <p> Всего цветов: {len(flower_list)} </p>
    <p> Полный список: {flower_list} </p>
    </body>
</html>
'''

@app.route('/lab2/add_flower/')
def no_flower():
    return f'''
    <!DOCTYPE html>
        <html>
            <head>
                <title>Ошибка!</title>
                <link rel="stylesheet" href="/static/lab1/lab1.css">
            </head>
            <body>
                <p>вы не задали имя цветка!</p>
                <a href="/lab2/all_flowers">Посмотреть все цветы</a><br>
                <a href="/lab2/add_flower/">Добавить новый цветок</a>
            </body>
        </html>
        ''', 400

@app.route('/lab2/all_flowers/')
def all_flowers():
    all_flowers = ""
    for i in flower_list:
        all_flowers += f"<li>{i}</li>"

    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Список всех цветов</title>
            <link rel="stylesheet" href="/static/lab1/lab1.css">
        </head>
        <body>
            <h1>Все цветы</h1>
            <p>Количество цветов: {len(flower_list)}</p>
            <ul>
                {all_flowers}
            </ul>
            <a href="/lab2/add_flower/">Добавить новый цветок</a>
        </body>
    </html>
    '''

@app.route('/lab2/delete_flowers')
def del_flowers():
    flower_list.clear()
    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Список цветов очищен</title>
            <link rel="stylesheet" href="/static/lab1/lab1.css">
        </head>
        <body>
            <h1>Список цветов был очищен</h1>
            <p>Все цветы удалены.</p>
            <a href="/lab2/all_flowers">Посмотреть список цветов</a>
        </body>
    </html>
    '''

@app.route('/lab2/example')
def example():

    name, number, group, course = 'Янсон Андрей', 2, 'ФБИ-21', 3
    fruits = [
        {'name': 'яблок', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321},
    ]
    return render_template('example.html',
                           name=name, number=number, group=group,
                           course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О сколько нам открытий чудных..."
    return render_template('filter.html', phrase=phrase)