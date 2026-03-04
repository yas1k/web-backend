from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import math
from sqlalchemy.orm import sessionmaker

from db import db
from db.models_rgz import Employee, HRUser
from flask import current_app

rgz = Blueprint('rgz', __name__)

ITEMS_PER_PAGE = 20

# ============== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==============
def get_rgz_session():
    """Возвращает сессию для БД rgz"""
    engine = db.get_engine(current_app._get_current_object(), bind='rgz')
    Session = sessionmaker(bind=engine)
    return Session()

# ============== СТРАНИЦЫ ==============

@rgz.route('/rgz/')
def index():
    """Главная страница со списком сотрудников"""
    return render_template('rgz/index.html', 
                         is_auth=current_user.is_authenticated,
                         user=current_user if current_user.is_authenticated else None)

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    """Страница входа для кадровика"""
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return render_template('rgz/login.html', error='Заполните все поля')
    
    # Получаем отдельную сессию для rgz
    session_rgz = get_rgz_session()
    user = session_rgz.query(HRUser).filter_by(username=username).first()
    session_rgz.close()
    
    if not user or not check_password_hash(user.password, password):
        return render_template('rgz/login.html', error='Неверный логин или пароль')
    
    login_user(user, remember=True)
    return redirect(url_for('rgz.index'))

@rgz.route('/rgz/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('rgz.index'))

@rgz.route('/rgz/employee/<int:id>')
def employee_card(id):
    """Страница карточки сотрудника"""
    session_rgz = get_rgz_session()
    employee = session_rgz.query(Employee).get(id)
    session_rgz.close()
    
    if not employee:
        return "Сотрудник не найден", 404
        
    return render_template('rgz/employee_card.html', 
                         employee=employee,
                         is_auth=current_user.is_authenticated)

@rgz.route('/rgz/employee/new', methods=['GET', 'POST'])
@login_required
def employee_new():
    """Создание нового сотрудника"""
    if request.method == 'GET':
        return render_template('rgz/employee_form.html', employee=None)
    
    data = request.form
    try:
        if not data.get('full_name') or not data.get('position'):
            raise ValueError('Заполните обязательные поля')
        
        employee = Employee(
            full_name=data['full_name'],
            position=data['position'],
            gender=data['gender'],
            phone=data['phone'],
            email=data['email'],
            probation='probation' in data,
            hire_date=datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
        )
        
        session_rgz = get_rgz_session()
        session_rgz.add(employee)
        session_rgz.commit()
        session_rgz.close()
        
        return redirect(url_for('rgz.index'))
    except Exception as e:
        return render_template('rgz/employee_form.html', 
                             error=str(e), employee=None)

@rgz.route('/rgz/employee/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def employee_edit(id):
    """Редактирование сотрудника"""
    session_rgz = get_rgz_session()
    employee = session_rgz.query(Employee).get(id)
    
    if request.method == 'GET':
        session_rgz.close()
        return render_template('rgz/employee_form.html', employee=employee)
    
    try:
        employee.full_name = request.form['full_name']
        employee.position = request.form['position']
        employee.gender = request.form['gender']
        employee.phone = request.form['phone']
        employee.email = request.form['email']
        employee.probation = 'probation' in request.form
        employee.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
        
        session_rgz.commit()
        session_rgz.close()
        return redirect(url_for('rgz.employee_card', id=id))
    except Exception as e:
        session_rgz.close()
        return render_template('rgz/employee_form.html', 
                             employee=employee, error=str(e))

@rgz.route('/rgz/employee/<int:id>/delete', methods=['POST'])
@login_required
def employee_delete(id):
    """Удаление сотрудника"""
    session_rgz = get_rgz_session()
    employee = session_rgz.query(Employee).get(id)
    
    if employee:
        session_rgz.delete(employee)
        session_rgz.commit()
    
    session_rgz.close()
    return redirect(url_for('rgz.index'))

# ============== REST API ==============

@rgz.route('/rgz/api/employees', methods=['GET'])
def api_employees():
    """API для получения списка сотрудников"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    sort_by = request.args.get('sort_by', 'id', type=str)
    sort_order = request.args.get('sort_order', 'asc', type=str)
    
    session_rgz = get_rgz_session()
    query = session_rgz.query(Employee)
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Employee.full_name.ilike(search_term),
                Employee.position.ilike(search_term),
                Employee.phone.ilike(search_term),
                Employee.email.ilike(search_term)
            )
        )
    
    if sort_order == 'asc':
        query = query.order_by(getattr(Employee, sort_by).asc())
    else:
        query = query.order_by(getattr(Employee, sort_by).desc())
    
    try:
        total = query.count()
        employees = query.offset((page - 1) * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE).all()
        
        result = {
            'employees': [emp.to_dict() for emp in employees],
            'total': total,
            'page': page,
            'pages': math.ceil(total / ITEMS_PER_PAGE),
            'per_page': ITEMS_PER_PAGE
        }
        
        session_rgz.close()
        return jsonify(result)
    except Exception as e:
        session_rgz.close()
        print(f"API Error: {e}")
        return jsonify({'error': str(e)}), 500

@rgz.route('/rgz/api/employee/<int:id>', methods=['GET'])
def api_employee(id):
    """API для получения одного сотрудника"""
    session_rgz = get_rgz_session()
    employee = session_rgz.query(Employee).get(id)
    session_rgz.close()
    
    if not employee:
        return jsonify({'error': 'Not found'}), 404
        
    return jsonify(employee.to_dict())