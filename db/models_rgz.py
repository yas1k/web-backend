from . import db
from flask_login import UserMixin
from datetime import datetime

class Employee(db.Model):
    """Модель сотрудника"""
    __bind_key__ = 'rgz'
    __tablename__ = 'rgz_employees'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # 'male', 'female'
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    probation = db.Column(db.Boolean, default=False)
    hire_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Преобразование в словарь для JSON"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'position': self.position,
            'gender': 'Мужской' if self.gender == 'male' else 'Женский',
            'phone': self.phone,
            'email': self.email,
            'probation': self.probation,
            'probation_text': 'Да' if self.probation else 'Нет',
            'hire_date': self.hire_date.strftime('%d.%m.%Y')
        }

class HRUser(db.Model, UserMixin):
    """Модель пользователя-кадровика"""
    __bind_key__ = 'rgz'
    __tablename__ = 'rgz_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(162), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)