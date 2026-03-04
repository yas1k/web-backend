-- Удалить всех сотрудников (таблица останется)
DELETE FROM rgz_employees;

-- Сбросить счетчик id, чтобы новые сотрудники начинали с 1
TRUNCATE TABLE rgz_employees RESTART IDENTITY;


-- Таблица сотрудников
CREATE TABLE rgz_employees (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    probation BOOLEAN DEFAULT FALSE,
    hire_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица пользователей-кадровиков
CREATE TABLE rgz_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(162) NOT NULL,
    full_name VARCHAR(100) NOT NULL
);

-- Генерируем 100 тестовых сотрудников
INSERT INTO rgz_employees (full_name, position, gender, phone, email, probation, hire_date)
SELECT 
    'Сотрудник ' || i,
    CASE (random() * 4)::int
        WHEN 0 THEN 'Менеджер'
        WHEN 1 THEN 'Разработчик'
        WHEN 2 THEN 'Тестировщик'
        WHEN 3 THEN 'Аналитик'
        ELSE 'Директор'
    END,
    CASE (random() > 0.5)::int WHEN 0 THEN 'male' ELSE 'female' END,
    '+7 (9' || (100 + i)::text || ') ' || LPAD(i::text, 3, '0'),
    'user' || i || '@company.ru',
    (random() > 0.7),
    CURRENT_DATE - (random() * 1000)::int
FROM generate_series(1, 102) i;


-- Добавляем тестового кадровика (пароль: admin123)
-- Хеш для 'admin123' нужно сгенерировать, пока вставим заглушку
INSERT INTO rgz_users (username, password, full_name) 
VALUES ('hr_admin', 'scrypt:32768:8:1$p2BqFzQjWkXmRnYp$3a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d', 'Администратор');

--Права доступа
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO rgz_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO rgz_user;