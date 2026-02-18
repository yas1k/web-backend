from flask import Blueprint, url_for, request, redirect, render_template, session, current_app
lab5 = Blueprint('lab5', __name__)
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path


@lab5.route('/lab5/')
def laba5():
    return render_template('lab5/lab5.html', login=session.get('login'))


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


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login%s;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/succes.html', login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login?;", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Логин и/или пароль неверны")
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Логин и/или пароль неверны")

    session['login'] = login
    db_close(conn, cur)

    return render_template('lab5/lab5.html', login=login)


@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute("SELECT * FROM articles WHERE user_id=%s;", (login_id,))
    articles = cur.fetchall()

    db_close(conn, cur)



    return render_template('lab5/articles.html', articles=articles)




@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'

    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Название и текст статьи не могут быть пустыми.")

    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute("INSERT INTO articles(user_id, title, article_text, is_public, is_favorite) VALUES (%s, %s, %s, %s, %s);", 
                (login_id, title, article_text, is_public, is_favorite))

    db_close(conn, cur)

    return redirect('/lab5')

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')



@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    article = cur.fetchone()


    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = request.form.get('is_public') == 'on'
        is_favorite = request.form.get('is_favorite') == 'on'

        cur.execute(
            "UPDATE articles SET title=%s, article_text=%s, is_public=%s, is_favorite=%s WHERE id=%s;",
            (title, article_text, is_public, is_favorite, article_id)
        )
        db_close(conn, cur)
        return redirect('/lab5')

    db_close(conn, cur)
    return render_template('lab5/edit.article.html', article=article)



@lab5.route('/lab5/delete/<int:article_id>')
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    cur.execute("DELETE FROM articles WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s);", (article_id, login))
    db_close(conn, cur)

    return redirect('/lab5/list')


@lab5.route('/lab5/user_logins')
def user_logins():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users;")
    else:
        cur.execute("SELECT login FROM users;")

    users = [row['login'] for row in cur.fetchall()]
    db_close(conn, cur)

    return render_template('lab5/user_logins.html', users=users)


@lab5.route('/lab5/public_articles')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT a.title, a.article_text, u.login FROM articles a JOIN users u ON a.user_id = u.id WHERE a.is_public=true;"
        )
    else:
        cur.execute(
            "SELECT a.title, a.article_text, u.login FROM articles a JOIN users u ON a.user_id = u.id WHERE a.is_public=1;"
        )

    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/public.articles.html', articles=articles)
