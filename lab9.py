from flask import Blueprint, render_template, session, jsonify, request, current_app, redirect
import random
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab9 = Blueprint('lab9', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='andrey_yanson_knowledge_base',
            user='andrey_yanson_knowledge_base',
            password='123',
            client_encoding='UTF8'
        )

        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def is_authenticated():
    """Проверка авторизации пользователя"""
    return 'lab9_user_authenticated' in session and session['lab9_user_authenticated']

def generate_non_overlapping_positions():
    """Генерация непересекающихся позиций для коробок"""
    positions = []
    attempts = 0
    max_attempts = 2000
    
    box_width = 18  
    box_height = 22 
    
    while len(positions) < 10 and attempts < max_attempts:
        top = random.randint(2, 87 - box_height)  
        left = random.randint(2, 87 - box_width)  

        overlap = False
        for (existing_top, existing_left) in positions:
            if (abs(top - existing_top) < box_height and 
                abs(left - existing_left) < box_width):
                overlap = True
                break
        
        if not overlap:
            positions.append((top, left))
        
        attempts += 1

    # Если не удалось сгенерировать 10 непересекающихся позиций
    while len(positions) < 10:
        top = random.randint(3, 87 - box_height)
        left = random.randint(3, 87 - box_width)
        positions.append((top, left))
    
    return positions


@lab9.route('/lab9/')
def main():
    conn, cur = db_connect()

    # Генерируем уникальный ID для пользователя
    if 'lab9_user_id' not in session:
        session['lab9_user_id'] = str(uuid.uuid4())
    
    user_id = session['lab9_user_id']
    is_auth = is_authenticated()

    # Создаем запись пользователя, если её нет
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT 1 FROM lab9_users WHERE id = %s", (user_id,))
    else:
        cur.execute("SELECT 1 FROM lab9_users WHERE id = ?", (user_id,))
    
    if not cur.fetchone():
        # Если пользователь авторизован, связываем с аккаунтом
        auth_user_id = session.get('lab9_auth_user_id')
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO lab9_users (id, auth_user_id) VALUES (%s, %s)", 
                       (user_id, auth_user_id))
        else:
            cur.execute("INSERT INTO lab9_users (id, auth_user_id) VALUES (?, ?)", 
                       (user_id, auth_user_id))

    # Создаем подарки для пользователя, если их нет
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = %s", (user_id,))
    else:
        cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = ?", (user_id,))
    
    gift_count = cur.fetchone()['cnt']
    
    if gift_count == 0:
        congratulations = [
            "С Новым Годом, правда, к сожалению вам достался подарок на 23 февраля!",
            "С праздником! Вам крупно повезло, вы получили в подарок письмо из Хогвартса!",
            "Желаю вам оставить в этом мире след! Как его оставил подаренный вам старенький айфон",
            "Букетик сушенной рыбки :) Разве не приятно?",
            "Пусть вы будете так же желанны, как первый домашний питомец у ребенка",
            "Хорошего вам праздника! Пусть всё получится! (P.S. деньги фальшивые, бантик вернете)",
            "Пусть всё будет у вас будет хорошо! :)",
            "Желаю такой же сладкой жизни, как эта коробочка",
            "К сожалению подарки заканчивались... Не расстраивайтесь, в Новом Году всё обязательно будет лучше!",
            "Пусть Новый год будет таким же ярким, как эти...странные носки..?"
        ]
        

        gift_images = [
            "/static/lab9/gifts/gift1.jpg",  
            "/static/lab9/gifts/gift2.jpg",  
            "/static/lab9/gifts/gift3.jpg",  
            "/static/lab9/gifts/gift4.jpg",  
            "/static/lab9/gifts/gift5.jpg",  
            "/static/lab9/gifts/gift6.jpg",  
            "/static/lab9/gifts/gift7.jpg",  
            "/static/lab9/gifts/gift8.jpg",  
            "/static/lab9/gifts/gift9.jpg",  
            "/static/lab9/gifts/gift10.jpg"  
        ]
        
        box_images = [
            "/static/lab9/boxes/box1.png",   
            "/static/lab9/boxes/box2.png",   
            "/static/lab9/boxes/box3.png",   
            "/static/lab9/boxes/box4.png",   
            "/static/lab9/boxes/box5.png",    
            "/static/lab9/boxes/box6.png",   
            "/static/lab9/boxes/box7.png",   
            "/static/lab9/boxes/box8.png",   
            "/static/lab9/boxes/box9.png",   
            "/static/lab9/boxes/box10.png"   
        ]
        
        # Генерируем непересекающиеся позиции
        positions = generate_non_overlapping_positions()
        
        for i in range(10):
            top_pos, left_pos = positions[i]
            # Первые 5 подарков доступны всем, последние 5 - только авторизованным
            require_auth = i >= 5
            
            params = (user_id, i, top_pos, left_pos,
                     congratulations[i], gift_images[i], box_images[i], require_auth)
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    INSERT INTO lab9_gifts 
                    (user_id, position_id, top_position, left_position, message, image, box_image, require_auth)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, params)
            else:
                cur.execute("""
                    INSERT INTO lab9_gifts 
                    (user_id, position_id, top_position, left_position, message, image, box_image, require_auth)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, params)

    # Получаем все подарки пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT position_id, top_position, left_position, opened, message, image, box_image, require_auth 
            FROM lab9_gifts WHERE user_id = %s ORDER BY position_id
        """, (user_id,))
    else:
        cur.execute("""
            SELECT position_id, top_position, left_position, opened, message, image, box_image, require_auth 
            FROM lab9_gifts WHERE user_id = ? ORDER BY position_id
        """, (user_id,))
    
    gifts = cur.fetchall()
    
    # Считаем открытые подарки
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = %s AND opened = TRUE", (user_id,))
    else:
        cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = ? AND opened = TRUE", (user_id,))
    
    opened_count = cur.fetchone()['cnt']
    
    db_close(conn, cur)
    
    return render_template('lab9/index.html',
                         gifts=gifts,
                         opened_count=opened_count,
                         remaining=10 - opened_count,
                         is_auth=is_auth,
                         login=session.get('lab9_login'))



@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    """Открытие подарка (AJAX запрос)"""
    user_id = session.get('lab9_user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})
    
    is_auth = is_authenticated()
    data = request.json
    gift_id = data.get('gift_id')
    
    conn, cur = db_connect()
    
    try:
        # Проверяем подарок
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT require_auth, opened 
                FROM lab9_gifts 
                WHERE user_id = %s AND position_id = %s
            """, (user_id, gift_id))
        else:
            cur.execute("""
                SELECT require_auth, opened 
                FROM lab9_gifts 
                WHERE user_id = ? AND position_id = ?
            """, (user_id, gift_id))
        
        gift_info = cur.fetchone()
        
        if not gift_info:
            return jsonify({'success': False, 'message': 'Подарок не найден'})
        
        # Проверка на авторизацию для специальных подарков
        if gift_info['require_auth'] and not is_auth:
            return jsonify({
                'success': False,
                'message': 'Войдите в систему, чтобы открыть этот подарок!'
            })
        
        # Проверка, открыт ли уже подарок
        if gift_info['opened']:
            return jsonify({'success': False, 'message': 'Этот подарок уже открыт!'})
        
        # Проверка лимита в 3 коробки
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT COUNT(*) as count 
                FROM lab9_gifts 
                WHERE user_id = %s AND opened = TRUE
            """, (user_id,))
        else:
            cur.execute("""
                SELECT COUNT(*) as count 
                FROM lab9_gifts 
                WHERE user_id = ? AND opened = TRUE
            """, (user_id,))
        
        opened_result = cur.fetchone()
        opened_count = opened_result['count']
        
        if opened_count >= 3:
            return jsonify({
                'success': False,
                'message': 'Вы уже открыли максимальное количество подарков (3)!'
            })
        
        # Открываем подарок
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE lab9_gifts 
                SET opened = TRUE 
                WHERE user_id = %s AND position_id = %s
                RETURNING message, image
            """, (user_id, gift_id))
        else:
            cur.execute("""
                UPDATE lab9_gifts 
                SET opened = TRUE 
                WHERE user_id = ? AND position_id = ?
            """, (user_id, gift_id))
            cur.execute("""
                SELECT message, image 
                FROM lab9_gifts 
                WHERE user_id = ? AND position_id = ?
            """, (user_id, gift_id))
        
        result = cur.fetchone()
        
        new_opened_count = opened_count + 1
        remaining = 10 - new_opened_count
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': result['message'],
            'image': result['image'],
            'opened_count': new_opened_count,
            'remaining': remaining
        })
        
    except Exception as e:
        print(f"Ошибка при открытии подарка: {e}")
        conn.rollback()
        return jsonify({'success': False, 'message': f'Ошибка при открытии подарка: {str(e)}'})
    finally:
        db_close(conn, cur)


@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    if request.method == 'GET':
        return render_template('lab9/login.html')
    
    login_val = request.form.get('login')
    password = request.form.get('password')
    
    if not login_val or not password:
        return render_template('lab9/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    try:
        # Ищем пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, password FROM lab9_auth_users WHERE login = %s", (login_val,))
        else:
            cur.execute("SELECT id, password FROM lab9_auth_users WHERE login = ?", (login_val,))
        
        user = cur.fetchone()
        
        if not user:
            return render_template('lab9/login.html', error='Неверный логин или пароль')
        
        # Проверяем пароль
        if not check_password_hash(user['password'], password):
            return render_template('lab9/login.html', error='Неверный логин или пароль')
        
        # Сохраняем в сессии
        session['lab9_user_authenticated'] = True
        session['lab9_login'] = login_val
        session['lab9_auth_user_id'] = user['id']
        
        # Обновляем запись пользователя, если она есть
        if 'lab9_user_id' in session:
            user_id = session['lab9_user_id']
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE lab9_users 
                    SET auth_user_id = %s 
                    WHERE id = %s
                """, (user['id'], user_id))
            else:
                cur.execute("""
                    UPDATE lab9_users 
                    SET auth_user_id = ? 
                    WHERE id = ?
                """, (user['id'], user_id))
        
        return redirect('/lab9/')
        
    except Exception as e:
        print(f"Ошибка при входе: {e}")
        return render_template('lab9/login.html', error=f'Ошибка: {str(e)}')
    finally:
        db_close(conn, cur)


@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    if request.method == 'GET':
        return render_template('lab9/register.html')
    
    login_val = request.form.get('login')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([login_val, password, confirm_password]):
        return render_template('lab9/register.html', error='Заполните все поля')
    
    if password != confirm_password:
        return render_template('lab9/register.html', error='Пароли не совпадают')
    
    if len(password) < 4:
        return render_template('lab9/register.html', error='Пароль должен быть не менее 4 символов')
    
    conn, cur = db_connect()
    
    try:
        # Проверяем, существует ли логин
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM lab9_auth_users WHERE login = %s", (login_val,))
        else:
            cur.execute("SELECT id FROM lab9_auth_users WHERE login = ?", (login_val,))
        
        if cur.fetchone():
            return render_template('lab9/register.html', error='Логин уже занят')
        
        # Хешируем пароль
        password_hash = generate_password_hash(password)
        
        # Создаем пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO lab9_auth_users (login, password) 
                VALUES (%s, %s) RETURNING id
            """, (login_val, password_hash))
            user_id = cur.fetchone()['id']
        else:
            cur.execute("""
                INSERT INTO lab9_auth_users (login, password) 
                VALUES (?, ?)
            """, (login_val, password_hash))
            user_id = cur.lastrowid
        
        # Сохраняем в сессии
        session['lab9_user_authenticated'] = True
        session['lab9_login'] = login_val
        session['lab9_auth_user_id'] = user_id
        
        # Обновляем запись пользователя, если она есть
        if 'lab9_user_id' in session:
            lab9_user_id = session['lab9_user_id']
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE lab9_users 
                    SET auth_user_id = %s 
                    WHERE id = %s
                """, (user_id, lab9_user_id))
            else:
                cur.execute("""
                    UPDATE lab9_users 
                    SET auth_user_id = ? 
                    WHERE id = ?
                """, (user_id, lab9_user_id))
        
        conn.commit()
        return redirect('/lab9/')
        
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        conn.rollback()
        return render_template('lab9/register.html', error=f'Ошибка: {str(e)}')
    finally:
        db_close(conn, cur)


@lab9.route('/lab9/logout')
def logout():
    """Выход из системы"""
    session.pop('lab9_user_authenticated', None)
    session.pop('lab9_login', None)
    session.pop('lab9_auth_user_id', None)
    return redirect('/lab9/')



@lab9.route('/lab9/santa', methods=['POST'])
def santa():
    """Кнопка Деда Мороза - сброс всех подарков"""
    if not is_authenticated():
        return jsonify({'success': False, 'message': 'Только для авторизованных пользователей!'})
    
    user_id = session.get('lab9_user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Пользователь не найден'})
    
    conn, cur = db_connect()
    
    try:
        # Генерируем новые позиции
        positions = generate_non_overlapping_positions()
        
        # Сбрасываем все подарки и обновляем позиции
        if current_app.config['DB_TYPE'] == 'postgres':
            for i in range(10):
                top_pos, left_pos = positions[i]
                cur.execute("""
                    UPDATE lab9_gifts 
                    SET opened = FALSE, 
                        top_position = %s, 
                        left_position = %s
                    WHERE user_id = %s AND position_id = %s
                """, (top_pos, left_pos, user_id, i))
        else:
            for i in range(10):
                top_pos, left_pos = positions[i]
                cur.execute("""
                    UPDATE lab9_gifts 
                    SET opened = 0, 
                        top_position = ?, 
                        left_position = ?
                    WHERE user_id = ? AND position_id = ?
                """, (top_pos, left_pos, user_id, i))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Для вас обновились подарки!'
        })
        
    except Exception as e:
        print(f"Ошибка при сбросе подарков: {e}")
        conn.rollback()
        return jsonify({'success': False, 'message': 'Ошибка при сбросе подарков'})
    finally:
        db_close(conn, cur)