-- ==========================================
-- резервная копия базы данных ShopDB
-- создано утилитой pg-buddy
-- дата создания: 2026-06-12 12:55:29
-- ==========================================

SET session_replication_role = 'replica';

DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- Структура таблицы categories
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Данные таблицы categories
INSERT INTO categories (id, name, description, created_at) VALUES (1, 'Электроника', 'Смартфоны, ноутбуки, аксессуары и гаджеты', '2026-06-10T16:17:59.338785');
INSERT INTO categories (id, name, description, created_at) VALUES (2, 'Книги', 'Художественная литература, учебники, программирование', '2026-06-10T16:17:59.338785');
INSERT INTO categories (id, name, description, created_at) VALUES (3, 'Одежда', 'Мужская и женская одежда, обувь', '2026-06-10T16:17:59.338785');
INSERT INTO categories (id, name, description, created_at) VALUES (4, 'Дом и кухня', 'Товары для дома, посуда, мелкая бытовая техника', '2026-06-10T16:17:59.338785');

-- Структура таблицы products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price NUMERIC(12, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Данные таблицы products
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (1, 1, 'Смартфон', 'Флагманский смартфон с великолепной камерой', 79990.00, 15, '2026-06-10T16:17:59.338785');
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (2, 1, 'Ноутбук MacroBook Air', 'Легкий и мощный рабочий ноутбук', 124990.00, 8, '2026-06-10T16:17:59.338785');
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (3, 1, 'Беспроводные наушники ', 'Наушники с активным шумоподавлением', 12500.00, 45, '2026-06-10T16:17:59.338785');
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (4, 2, 'Изучаем Python, Марк Лутц', 'Лучшее руководство по языку Python', 4500.00, 20, '2026-06-10T16:17:59.338785');
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (5, 2, 'Чистый код, Роберт Мартин', 'Создание, анализ и рефакторинг кода', 1800.00, 30, '2026-06-10T16:17:59.338785');
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (6, 3, 'Футболка Хлопок', 'Базовая белая футболка, 100% хлопок', 1200.00, 100, '2026-06-10T16:17:59.338785');
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (7, 3, 'Худи  Черный', 'Теплая толстовка свободного кроя', 3500.00, 40, '2026-06-10T16:17:59.338785');
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (8, 4, 'Электрический чайник', 'Чайник с возможностью управления со смартфона', 4200.00, 12, '2026-06-10T16:17:59.338785');
INSERT INTO products (id, category_id, name, description, price, stock, created_at) VALUES (9, 4, 'Набор керамических ножей', 'Острые долговечные ножи для кухни (5 шт.)', 2500.00, 25, '2026-06-10T16:17:59.338785');

-- Структура таблицы customers
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Данные таблицы customers
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (1, 'Александр', 'Петров', 'petrov.alex@email.com', '+79991234567', 'г. Москва, ул. Ленина, д. 10, кв. 42', '2026-06-10T16:17:59.338785');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (2, 'Мария', 'Иванова', 'ivanova.maria@email.com', '+79997654321', 'г. Санкт-Петербург, Невский пр., д. 5, кв. 12', '2026-06-10T16:17:59.338785');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (3, 'Дмитрий', 'Смирнов', 'smirnov.dima@email.com', '+79883332211', 'г. Новосибирск, ул. Кирова, д. 50, кв. 3', '2026-06-10T16:17:59.338785');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (4, 'Елена', 'Кузнецова', 'kuznec.elena@email.com', '+79004445566', 'г. Екатеринбург, ул. Малышева, д. 25, кв. 115', '2026-06-10T16:17:59.338785');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (5, 'Станислав', 'Кудрявцев', 'evdokim1987@example.net', '8 054 532 26 72', 'г. Верхоянск, ул. Терешковой, д. 8/3 стр. 562, 930691', '2026-06-10T18:03:28.810882');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (6, 'Николай', 'Шубина', 'marfa75@example.net', '+71210537740', 'ст. Стрежевой, пер. Алтайский, д. 43, 390040', '2026-06-10T18:03:56.366206');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (7, 'Эрнст', 'Игнатьева', 'cveselov@example.org', '80675461942', 'к. Тулун, пер. Лунный, д. 9/6 к. 1, 221025', '2026-06-10T18:03:56.366206');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (8, 'Василий', 'Васильев', 'vasilyev.vas@email.com', '+79927654321', 'г. Москва, ул. Арбат, д. 1, кв. 2', '2026-06-12T16:17:59.338785');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (9, 'Екатерина', 'Иванова', 'ivanova.ekaterina@email.com', '+79997635321', 'г. Санкт-Петербург, Победы пр., д. 2, кв. 1', '2026-06-12T12:17:59.338785');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (10, 'Виталий', 'Котов', 'nikifor_1996@example.net', '8 895 853 53 55', 'п. Моршанск, алл. Сибирская, д. 67 к. 5/8, 985410', '2026-06-12T12:52:02.097008');
INSERT INTO customers (id, first_name, last_name, email, phone, address, created_at) VALUES (11, 'Сидор', 'Нестеров', 'marinagavrilova@example.com', '85657171320', 'д. Асбест, наб. Щербакова, д. 5 к. 10, 473017', '2026-06-12T12:52:02.097008');

-- Структура таблицы orders
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Новый',
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Данные таблицы orders
INSERT INTO orders (id, customer_id, status, total_amount, created_at) VALUES (1, 1, 'Оплачен', 92490.00, '2026-06-08T14:30:00');
INSERT INTO orders (id, customer_id, status, total_amount, created_at) VALUES (2, 2, 'Доставлен', 7500.00, '2026-06-09T10:15:00');
INSERT INTO orders (id, customer_id, status, total_amount, created_at) VALUES (3, 3, 'Новый', 4200.00, '2026-06-10T12:00:00');
INSERT INTO orders (id, customer_id, status, total_amount, created_at) VALUES (4, 5, 'Оплачен', 7000.00, '2026-05-24T16:29:14');

-- Структура таблицы order_items
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price NUMERIC(12, 2) NOT NULL
);

-- Данные таблицы order_items
INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES (1, 1, 1, 1, 79990.00);
INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES (2, 1, 3, 1, 12500.00);
INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES (3, 2, 4, 1, 4500.00);
INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES (4, 2, 5, 1, 1800.00);
INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES (5, 2, 6, 1, 1200.00);
INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES (6, 3, 8, 1, 4200.00);
INSERT INTO order_items (id, order_id, product_id, quantity, price) VALUES (7, 4, 7, 2, 3500.00);

SET session_replication_role = 'origin';