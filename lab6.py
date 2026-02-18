import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app
from os import path
import sqlite3
from flask import Blueprint, render_template, request, session, url_for

lab6 = Blueprint('lab6', __name__)



@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')