from flask import Blueprint, render_template, request, abort, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app
from os import path
import sqlite3
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

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


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')