
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- таблица категории
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- таблица товаров
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- таблица клиентов
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- таблица заказов
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL DEFAULT 'Новый' CHECK (status IN ('Новый', 'Оплачен', 'Доставляется', 'Доставлен', 'Отменен')),
    total_amount NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- таблица содержимого заказа
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity > 0),
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0)
);



-- вставка категорий
INSERT INTO categories (name, description) VALUES
('Электроника', 'Смартфоны, ноутбуки, аксессуары и гаджеты'),
('Книги', 'Художественная литература, учебники, программирование'),
('Одежда', 'Мужская и женская одежда, обувь'),
('Дом и кухня', 'Товары для дома, посуда, мелкая бытовая техника');

-- вставка товаров
INSERT INTO products (category_id, name, description, price, stock) VALUES
(1, 'Смартфон', 'Флагманский смартфон с великолепной камерой', 79990.00, 15),
(1, 'Ноутбук MacroBook Air', 'Легкий и мощный рабочий ноутбук', 124990.00, 8),
(1, 'Беспроводные наушники ', 'Наушники с активным шумоподавлением', 12500.00, 45),
(2, 'Изучаем Python, Марк Лутц', 'Лучшее руководство по языку Python', 4500.00, 20),
(2, 'Чистый код, Роберт Мартин', 'Создание, анализ и рефакторинг кода', 1800.00, 30),
(3, 'Футболка Хлопок', 'Базовая белая футболка, 100% хлопок', 1200.00, 100),
(3, 'Худи  Черный', 'Теплая толстовка свободного кроя', 3500.00, 40),
(4, 'Электрический чайник', 'Чайник с возможностью управления со смартфона', 4200.00, 12),
(4, 'Набор керамических ножей', 'Острые долговечные ножи для кухни (5 шт.)', 2500.00, 25);

-- вставка клиентов
INSERT INTO customers (first_name, last_name, email, phone, address) VALUES
('Александр', 'Петров', 'petrov.alex@email.com', '+79991234567', 'г. Москва, ул. Ленина, д. 10, кв. 42'),
('Мария', 'Иванова', 'ivanova.maria@email.com', '+79997654321', 'г. Санкт-Петербург, Невский пр., д. 5, кв. 12'),
('Дмитрий', 'Смирнов', 'smirnov.dima@email.com', '+79883332211', 'г. Новосибирск, ул. Кирова, д. 50, кв. 3'),
('Елена', 'Кузнецова', 'kuznec.elena@email.com', '+79004445566', 'г. Екатеринбург, ул. Малышева, д. 25, кв. 115');

-- вставка заказов
-- заказ 1: александр петров покупает смартфон и наушники
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(1, 'Оплачен', 92490.00, '2026-06-08 14:30:00');

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 79990.00), -- смартфон
(1, 3, 1, 12500.00); -- беспроводные наушники

-- Заказ 2: мария иванова покупает книги и футболку
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(2, 'Доставлен', 7500.00, '2026-06-09 10:15:00');

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(2, 4, 1, 4500.00), -- книга Марка Лутца
(2, 5, 1, 1800.00), -- книга Роберта Мартина
(2, 6, 1, 1200.00); -- футболка

-- Заказ 3: дмитрий смирнов делает новый заказ на чайник
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(3, 'Новый', 4200.00, '2026-06-10 12:00:00');

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(3, 8, 1, 4200.00); -- чайник
