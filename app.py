from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/web")
def web():
    return """<!doctype html>\
        <html>\
            <body>\
                <h1>web-сервер на flask</h1>\
                <a href="/author">author</a>\
                <a href="/lab1/oak">oak</a>\
                <a href="/lab1/counter">counter</a>\
                <a href="/lab1/created">created</a>\
            </body>\
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/author")
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
                <a href="/web">web</a>
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
            <a href="/web">web</a>
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
            <a href="/web">web</a>
            <a href="/lab1/erase">erase</a>
        </body>
    </html>
    '''

@app.route("/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return'''
    <!doctype html>
    <html>
        <body>
            <h1> Создано успешно</h1>
            <div><i>что-то создано...</i></div>
            <a href="/web">web</a>
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