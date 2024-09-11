from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/index")
def index():
    return '''
    <!doctype html>
    <html>
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
        <head>
            <title> НГТУ, ФБ, Лабораторные работы </title>
        </head>
        <body>
            <main>
                <p> Flask - фреймворк для создания веб-приложений на языке программирования
                Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
                Относится к категории так называемых микрофреймворков - минималистичных каркасов
                веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
                </p>
                <a href ="/">Корень сайта</a>
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
        <link rel="stylesheet" href="static/lab1.css">
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
        <body>
            <h1> Создано успешно</h1>
            <div><i>что-то создано...</i></div>
            <a href="/lab1/web">web</a>
        </body>
    </html>
    ''', 201

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

@app.route("/lab1/erase")
def erase():
    global count
    count = 0
    return'''
    <!doctype html>
    <html>
        <body>
            <h1>Счетчик обнулен</h1>
            <a href="/lab1/counter">counter</a>
        </body>
    </html>'''