CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(162) NOT NULL
);

CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    title VARCHAR(50),
    article_text TEXT,
    is_favorite BOOLEAN,
    is_public BOOLEAN,
    likes INTEGER
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO andrey_yanson_knowledge_base;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO andrey_yanson_knowledge_base;

CREATE TABLE offices (
    id SERIAL PRIMARY KEY,
    number INTEGER NOT NULL UNIQUE,
    tenant VARCHAR(30) DEFAULT ''
);

-- Добавим несколько офисов для теста
INSERT INTO offices (number, tenant) VALUES 
    (1, ''),
    (2, ''),
    (3, ''),
    (4, ''),
    (5, '');


ALTER TABLE offices ADD COLUMN price INTEGER DEFAULT 1000;
UPDATE offices SET price = 1000 + (number * 100);

GRANT ALL PRIVILEGES ON TABLE offices TO andrey_yanson_knowledge_base;
GRANT ALL PRIVILEGES ON SEQUENCE offices_id_seq TO andrey_yanson_knowledge_base;

CREATE TABLE films (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    title_ru VARCHAR(255),
    year INTEGER NOT NULL,
    description TEXT NOT NULL
);


INSERT INTO films (title, title_ru, year, description) VALUES
    ('The Shawshank Redemption', 'Побег из Шоушенка', 1994, 'Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и несправедливостью, окружающими заключённых.'),
    ('The Godfather', 'Крёстный отец', 1972, 'Криминальная сага, повествующая о нью-йоркской сицилийской мафиозной семье Корлеоне.'),
    ('Pulp Fiction', 'Криминальное чтиво', 1994, 'Несколько связанных историй из жизни бандитов, таинственных незнакомцев и простых американцев.'),
    ('The Dark Knight', 'Тёмный рыцарь', 2008, 'Бэтмен поднимает ставки в войне с преступностью. С помощью лейтенанта Джима Гордона и прокурора Харви Дента он намерен очистить улицы Готэма от преступности.'),
    ('Inception', 'Начало', 2010, 'Кобб — талантливый вор, лучший из лучших в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна.');

GRANT ALL PRIVILEGES ON TABLE films TO andrey_yanson_knowledge_base;
GRANT ALL PRIVILEGES ON SEQUENCE films_id_seq TO andrey_yanson_knowledge_base;