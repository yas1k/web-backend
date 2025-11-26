from flask import Blueprint, url_for, redirect, render_template, abort

lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a():

    return 'без слэша'

@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f'''
    <!doctype html>
    <html>
        <body>
        <h1> Вы успешно выбрали конкретный цветок из списка </h1>
        <p>Выбранный вами цветок: {flower_list[flower_id]}
        <a href ="/lab2/all_flowers">Все цветы</a>
        </body>
    </html>
    
    '''

@lab2.route('/lab2/add_flower/<name>')
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

@lab2.route('/lab2/example')
def example():
    name, lab_num,  group,  course_num  ='Янсон Андрей', '2', 'ФБИ-31',  '3'
    fruits = [
        {'name': 'Яблоки', 'price': 100},
        {'name': 'Груши', 'price': 120},
        {'name': 'Апельсины', 'price': 80},
        {'name': 'Мандарины', 'price': 95},
        {'name': 'Манго', 'price': 321}
        ]
    return render_template('example.html', name=name, lab_num=lab_num, group=group, course_num=course_num, fruits=fruits)


@lab2.route('/lab2/')
def lab2_index():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О сколько нам открытий чудных..."
    return render_template('filter.html', phrase=phrase)

@lab2.route('/lab2/add_flower/')
def noname():
    return'''
    УЖАС! ВЫ ЗАБЫЛИ ЗАДАТЬ ИМЯ ЦВЕТКА! НА ЧТО ВЫ РАССЧИТЫВАЛИ?
    ''', 400

@lab2.route('/lab2/all_flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
    <p> Количество цветов: {len(flower_list)} </p>
    <p> Полный список всех цветов: {flower_list} </p>
    </body>
</html>
'''
@lab2.route('/lab2/no_flowers')
def no_flowers():
    global flower_list
    flower_list = []
    return f'''
    <p> Вы очистили список цветов </p>
    <a href ="/lab2/all_flowers">Все цветы</a>
'''

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calculate(a, b):
    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Калькулятор</title>
        </head>
        <body>
            <h1>Расчёт с параметрами:</h1>
            <p>{a} + {b} = {a + b}</p>
            <p>{a} - {b} = {a - b}</p>
            <p>{a} * {b} = {a * b}</p>
            <p>{a} / {b} = {(a / b) if b != 0 else 'Деление на ноль'}</p>
            <p>{a}<sup>{b}</sup> = {a ** b}</p>
        </body>
    </html>
    '''


@lab2.route('/lab2/calc/')
def calc():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>/')
def calc_one(a):
    return redirect(f'/lab2/calc/{a}/1')
    
books = [
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 470},
    {"author": "Лев Толстой", "title": "Анна Каренина", "genre": "Роман", "pages": 864},
    {"author": "Борис Пастернак", "title": "Доктор Живаго", "genre": "Роман", "pages": 704},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Поэма", "pages": 240},
    {"author": "Фёдор Достоевский", "title": "Идиот", "genre": "Роман", "pages": 640},
    {"author": "Иван Гончаров", "title": "Обломов", "genre": "Роман", "pages": 560},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Роман", "pages": 352},
    {"author": "Антон Чехов", "title": "Чайка", "genre": "Пьеса", "pages": 120}
]


@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

places = [
    {"name": "Собор Александра Невского", "description": "Был построен аж в 1899 году!", "image":"sobor.jfif"},
    {"name": "Театр оперы и балета", "description": "Самый большой театр России!", "image": "novat.jfif"},
    {"name": "Новосибирский зоопарк имени Р. А. Шило", "description": "Один из крупнейших зоопарков России, содержащий больше 11 тыс. животных.", "image": "zoo.jfif"},
    {"name": "Музей железнодорожной техники", "description": "Железная дорога и поезда сыграли немалую роль в развитии Новосибирска, поэтому заслужили собственный музей.", "image": "gd.jfif"},
    {"name": "Театр «Глобус»", "description": "Просто красивое место.", "image": "globus.jfif"}
]


@lab2.route('/lab2/places')
def show_places():
    return render_template('places.html', places=places)