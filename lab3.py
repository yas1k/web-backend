from flask import Blueprint, render_template, request, make_response, redirect
from datetime import datetime

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    return render_template('lab3/lab3.html')

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай — 80 рублей, зелёный — 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    # Добавка молока удорожает напиток на 30 рублей, а сахара — на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)  # Получаем цену из URL параметра
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    # Считываем параметры из запроса
    color = request.args.get('color')
    background = request.args.get('background')
    font_size = request.args.get('font_size')
    
    # Если параметры переданы, сохраняем их в куки
    if color or background or font_size:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background:
            resp.set_cookie('background', background)
        if font_size:
            resp.set_cookie('font_size', font_size)
        return resp

    color = request.cookies.get('color')
    background = request.cookies.get('background')
    font_size = request.cookies.get('font_size')
    return render_template('lab3/settings.html', color=color, background=background, font_size=font_size)

@lab3.route('/lab3/tickets')
def ticket_order():

    today = datetime.now().strftime('%Y-%m-%d')

    errors = {}

    seat = request.args.get('seat', '')  # Возвращаем пустую строку, если параметр не передан
    travel_date = request.args.get('travel_date', '')
    departure = request.args.get('departure')
    destination = request.args.get('destination')

    if departure == destination:
        errors['destination'] = 'Ошибка! Города не могут совпадать!'

        errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'


    return render_template('lab3/tickets.html', user=user, age=age, seat=seat, departure=departure, destination=destination, 
    travel_date=travel_date, today=today, errors=errors)


@lab3.route('/lab3/tickets_result')
def tickets_result():
    price = 0

    user = request.args.get('user')
    age = request.args.get('age')
    seat = request.args.get('seat')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    travel_date = request.args.get('travel_date')

    # Определяем, детский ли билет
    if int(age) < 18:
        is_child = True
        price += 700
    else:
        is_child = False
        price += 1000

    # Дополнительные цены
    if seat in ['lowwer', 'lowwer_side']:
        price += 100 
    if request.args.get('sheets') == 'on':
        price += 75 
    if request.args.get('baggage') == 'on':
        price += 250 
    if request.args.get('insurance') == 'on':
        price += 150 

    return render_template('lab3/ticket_result.html', user=user, age=age, seat=seat, departure=departure, 
    destination=destination, travel_date=travel_date,
     is_child=is_child, price=price)