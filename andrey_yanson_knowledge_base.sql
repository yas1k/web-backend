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

GRANT ALL PRIVILEGES ON TABLE offices TO andrey_yanson_knowledge_base;
GRANT ALL PRIVILEGES ON SEQUENCE offices_id_seq TO andrey_yanson_knowledge_base;
