from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/web")
def web():
    return """<!doctype html>\
        <html>\
            <body>\
                <h1>web-сервер на flask</h1>\
                <a href="/author">author</a>\
            </body>\
        </html>"""

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
    return '''
    <!doctype html>
    <html>
        <body>
            <h1>Дуб</h1>
            <img src="''' + path +  '''">
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
        </body>
    </html>
    '''

@app.route("/info")
def info():
    return redirect("/author")