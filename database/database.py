import sqlite3


class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('shop.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_users_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(100),
            phone TEXT,
            lang TEXT
        )
        '''
        self.manager(sql, commit=True)

    def get_user_by_id(self, telegram_id):
        sql = '''
        SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_user_lang(self, telegram_id):
        sql = '''
        SELECT lang FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)[0]

    def change_user_lang(self, telegram_id, lang):
        sql = '''
        UPDATE users SET lang = ? WHERE telegram_id = ?
        '''
        self.manager(sql, lang, telegram_id, commit=True)

    def update_user_phone(self, chat_id, phone):
        sql = '''
        UPDATE users SET phone = ? WHERE telegram_id = ?
        '''
        self.manager(sql, phone, chat_id, commit=True)

    def insert_user(self, telegram_id, full_name, lang):
        sql = '''
        INSERT INTO users(telegram_id, full_name, lang) VALUES (?,?,?)
        '''
        self.manager(sql, telegram_id, full_name, lang, commit=True)

    def create_main_categories_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS categories(
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_title_ru VARCHAR(50) UNIQUE,
            category_title_uz VARCHAR(50) UNIQUE
        )
        '''
        self.manager(sql, commit=True)

    def create_subcategories_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS subcategories(
            subcategory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subcategory_title_ru VARCHAR(50),
            subcategory_title_uz VARCHAR(50),
            category_id INTEGER REFERENCES categories(category_id)  ON DELETE CASCADE
        )
        '''
        self.manager(sql, commit=True)

    def create_firms_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS firms(
            firm_id INTEGER PRIMARY KEY AUTOINCREMENT,
            firm_title_ru VARCHAR(50),
            firm_title_uz VARCHAR(50),
            subcategory_id INTEGER REFERENCES subcategories(subcategory_id)  ON DELETE CASCADE
        )
        '''
        self.manager(sql, commit=True)

    def create_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_title_ru VARCHAR(50),
            product_title_uz VARCHAR(50),
            description_ru VARCHAR(255),
            description_uz VARCHAR(255),
            price INTEGER,
            image TEXT,
            firm_id INTEGER REFERENCES firms(firm_id)
        )
        '''
        self.manager(sql, commit=True)

    def get_all_categories(self):
        sql = '''
        SELECT * FROM categories 
        '''
        return self.manager(sql, fetchall=True)

    def get_category(self, category_id):
        sql = '''
        SELECT * FROM categories WHERE category_id = ?
        '''
        return self.manager(sql, category_id, fetchone=True)

    def get_subcategory(self, subcategory_id):
        sql = '''
        SELECT * FROM subcategories WHERE subcategory_id = ?
        '''
        return self.manager(sql, subcategory_id, fetchone=True)

    def get_firm(self, firm_id):
        sql = '''
        SELECT * FROM firms WHERE firm_id = ?
        '''
        return self.manager(sql, firm_id, fetchone=True)

    def create_new_category(self, category_title_ru, category_title_uz):
        sql = '''
        INSERT INTO categories(category_title_ru, category_title_uz) VALUES (?, ?)
        '''
        self.manager(sql, category_title_ru, category_title_uz, commit=True)

    def get_subcategory_by_firm_id(self, firm_id):
        sql = '''
        SELECT subcategory_id FROM firms WHERE firm_id = ?
        '''
        return self.manager(sql, firm_id, fetchone=True)[0]

    def get_category_id_by_subcategory_id(self, subcategory_id):
        sql = '''
        SELECT category_id FROM subcategories WHERE subcategory_id = ?
        '''
        return self.manager(sql, subcategory_id, fetchone=True)[0]

    def create_new_subcategory(self, category_ru, category_uz, category_id):
        sql = '''
        INSERT INTO subcategories(subcategory_title_ru, subcategory_title_uz, category_id) VALUES (?, ?, ?)
        '''
        self.manager(sql, category_ru, category_uz, category_id, commit=True)

    def create_new_firm(self, firm_ru, firm_uz, subcategory_id):
        sql = '''
        INSERT INTO firms(firm_title_ru, firm_title_uz, subcategory_id) VALUES (?, ?, ?)
        '''
        self.manager(sql, firm_ru, firm_uz, subcategory_id, commit=True)

    def delete_category(self, category_id):
        sql = '''
        DELETE FROM categories WHERE category_id = ?;
        '''
        self.manager(sql, category_id, commit=True)

    def delete_subcategory(self, subcategory_id):
        sql = '''
        DELETE FROM subcategories WHERE subcategory_id = ?;
        '''
        self.manager(sql, subcategory_id, commit=True)

    def delete_firm(self, firm_id):
        sql = '''
        DELETE FROM firms WHERE firm_id = ?;
        '''
        self.manager(sql, firm_id, commit=True)

    def get_subcategories_for_admin(self, category_id):
        sql = '''
        SELECT * FROM subcategories WHERE category_id = ?
        '''
        return self.manager(sql, category_id, fetchall=True)

    def get_firms_for_admin(self, subcategory_id):
        sql = '''
        SELECT * FROM firms WHERE subcategory_id = ?
        '''
        return self.manager(sql, subcategory_id, fetchall=True)

    def get_firms_for_user(self, subcategory_id):
        sql = '''
        SELECT * FROM firms WHERE subcategory_id = ?
        '''
        return self.manager(sql, subcategory_id, fetchall=True)

    def get_products_for_admin(self, firm_id):
        sql = '''
        SELECT * FROM products WHERE firm_id = ?;
        '''
        return self.manager(sql, firm_id, fetchall=True)

    def get_products_for_users(self, firm_id):
        sql = '''
        SELECT * FROM products WHERE firm_id = ?
        '''
        return self.manager(sql, firm_id, fetchall=True)

    def get_products_status_1(self):
        sql = '''
        SELECT product_title_ru FROM products
        '''
        return self.manager(sql, fetchall=True)

    def get_product_by_title(self, product_title):
        sql = '''
        SELECT * FROM products WHERE product_title = ?
        '''
        return self.manager(sql, product_title, fetchone=True)

    def get_product_detail_by_id(self, product_id):
        sql = '''
        SELECT * FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)

    def get_all_products(self):
        sql = '''
        SELECT product_title FROM products
        '''
        return self.manager(sql, fetchall=True)

    def create_cart_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart(
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER REFERENCES users(telegram_id),
            total_quantity INTEGER DEFAULT 0,
            total_price INTEGER DEFAULT 0
        )
        '''
        self.manager(sql, commit=True)

    def create_cart_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS cart_products(
            cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER REFERENCES cart(cart_id),
            product_name VARCHAR(100) NOT NULL,
            final_price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            
            UNIQUE(cart_id, product_name)
        )
        '''
        self.manager(sql, commit=True)

    def create_cart_for_user(self, telegram_id):
        sql = '''
        INSERT INTO cart(telegram_id) VALUES (?)
        '''
        self.manager(sql, telegram_id, commit=True)

    def get_cart_id(self, telegram_id):
        sql = '''
        SELECT cart_id FROM cart WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def get_product_by_id(self, product_id):
        sql = '''
        SELECT product_title_ru, product_title_uz, price FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)

    def insert_cart_product(self, cart_id, product_name, quantity, final_price):
        sql = '''
        INSERT INTO cart_products(cart_id, product_name, quantity, final_price)
        VALUES (?,?,?,?)
        '''
        self.manager(sql, cart_id, product_name, quantity, final_price, commit=True)

    def update_cart_product(self, cart_id, product_name, quantity, final_price):
        sql = '''
        UPDATE cart_products
        SET
        quantity = quantity + ?,
        final_price = final_price + ?
        WHERE product_name = ? AND cart_id = ?
        '''
        self.manager(sql, quantity, final_price, product_name, cart_id, commit=True)

    def update_cart_total_price_quantity(self, cart_id):
        sql = '''
        UPDATE cart
        SET
        total_quantity = (
            SELECT SUM(quantity) FROM cart_products WHERE cart_id = ?
        ),
        total_price = (
            SELECT SUM(final_price) FROM cart_products WHERE cart_id = ?
        )
        WHERE cart_id = ?
        '''
        self.manager(sql, cart_id, cart_id, cart_id, commit=True)

    def get_cart_total_price_quantity(self, cart_id):
        sql = '''
        SELECT total_price, total_quantity FROM cart WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchone=True)

    def get_cart_products_by_cart_id(self, cart_id):
        sql = '''
        SELECT * FROM cart_products WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchall=True)

    def delete_error(self, cart_product_id):
        sql = '''
        DELETE FROM cart_products WHERE cart_product_id = ?
        '''
        self.manager(sql, cart_product_id, commit=True)

    # def create_product_admin(self, name, price, description):
    #     sql = '''
    #     INSERT INTO
    #     '''

    def create_order_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER REFERENCES users(telegram_id),
            order_number_user INTEGER,
            location TEXT,
            status VARCHAR(50) DEFAULT 'Обработка',
            order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_quantity INTEGER DEFAULT 0,
            total_price INTEGER DEFAULT 0,
            money VARCHAR(255)
        )
        '''
        self.manager(sql, commit=True)

    def create_order_products_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS order_products(
            order_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER REFERENCES orders(order_id),
            product_name VARCHAR(100) NOT NULL,
            final_price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,

            UNIQUE(order_id, product_name)
        )
        '''
        self.manager(sql, commit=True)

    def get_count_orders_by_user(self, chat_id):
        sql = '''
        SELECT order_number_user FROM orders WHERE telegram_id = ?
        '''
        return self.manager(sql, chat_id, fetchall=True)

    def get_cart(self, cart_id):
        sql = '''
        SELECT * FROM cart WHERE cart_id = ?
        '''
        return self.manager(sql, cart_id, fetchone=True)

    def create_order(self, telegram_id, order_number_user, total_quantity, total_price, location, money):
        sql = '''
        INSERT INTO orders(telegram_id, order_number_user, total_quantity, total_price, order_time, location, money) VALUES (?,?,?,?, DATETIME('now', '+5 hours'), ?, ?)
         '''
        self.manager(sql, telegram_id, order_number_user, total_quantity, total_price, location, money, commit=True)

    def get_order_id(self, telegram_id, order_number_user):
        sql = '''
        SELECT order_id FROM orders WHERE telegram_id = ? AND order_number_user = ? 
        '''
        return self.manager(sql, telegram_id, order_number_user, fetchone=True)

    def create_new_order_product(self, order_id, product_name, final_price, quantity):
        sql = '''
        INSERT INTO order_products(order_id, product_name, final_price, quantity) VALUES (?,?,?,?)
        '''
        self.manager(sql, order_id, product_name, final_price, quantity, commit=True)

    def create_products(self, product_title_ru, product_title_uz, description_ru, description_uz, price, image,
                        firm_id):
        sql = '''
        INSERT INTO products(product_title_ru, product_title_uz, description_ru, description_uz, price, image, firm_id)
        VALUES
        (?,?,?,?,?,?,?)
        '''
        self.manager(sql, product_title_ru, product_title_uz, description_ru, description_uz, price, image, firm_id,
                     commit=True)

    def delete_product(self, product_id):
        sql = '''
        DELETE FROM products WHERE product_id = ?
        '''
        self.manager(sql, product_id, commit=True)

    def get_count_orders_1_month(self):
        sql = '''
        SELECT COUNT(*) AS order_count
            FROM orders
            WHERE order_time >= DATE('now', '-1 month');
        '''
        return self.manager(sql, fetchone=True)

    def get_today_morning(self):
        sql = '''
        SELECT * FROM orders
        WHERE DATE(order_time) = DATE('now', 'localtime')
            AND TIME(order_time) BETWEEN '01:00:00' AND '12:00:00'; 
        '''
        return self.manager(sql, fetchall=True)

    def get_today_day(self):
        sql = '''
        SELECT * FROM orders
WHERE 
  (DATE(order_time) = DATE('now', 'localtime') AND TIME(order_time) BETWEEN '12:00:00' AND '23:59:59')
  OR
  (DATE(order_time) = DATE('now', 'localtime', '+1 day') AND TIME(order_time) BETWEEN '00:00:00' AND '01:00:00');
        '''
        return self.manager(sql, fetchall=True)

    def get_count_orders_3_month(self):
        sql = '''
        SELECT COUNT(*) AS order_count
            FROM orders
            WHERE order_time >= DATE('now', '-3 month');
        '''
        return self.manager(sql, fetchone=True)

    def get_count_orders_6_month(self):
        sql = '''
        SELECT COUNT(*) AS order_count
            FROM orders
            WHERE order_time >= DATE('now', '-3 month');
        '''
        return self.manager(sql, fetchone=True)

    def get_count_orders_12_month(self):
        sql = '''
        SELECT COUNT(*) AS order_count
            FROM orders
            WHERE order_time >= DATE('now', '-12 month');
        '''
        return self.manager(sql, fetchone=True)

    def get_sum_of_price_orders1(self):
        sql = '''
        SELECT SUM(total_price) AS total_amount
FROM orders
WHERE order_time >= DATE('now', '-1 month');
        '''
        return self.manager(sql, fetchone=True)

    def get_sum_of_price_orders3(self):
        sql = '''
            SELECT SUM(total_price) AS total_amount
    FROM orders
    WHERE order_time >= DATE('now', '-3 month');
            '''
        return self.manager(sql, fetchone=True)

    def get_sum_of_price_orders6(self):
        sql = '''
            SELECT SUM(total_price) AS total_amount
    FROM orders
    WHERE order_time >= DATE('now', '-6 month');
            '''
        return self.manager(sql, fetchone=True)

    def get_sum_of_price_orders12(self):
        sql = '''
            SELECT SUM(total_price) AS total_amount
    FROM orders
    WHERE order_time >= DATE('now', '-12 month');
            '''
        return self.manager(sql, fetchone=True)

    def create_admins_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS admins(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(100),
            admin_type INTEGER DEFAULT 0
        )
        '''
        # 0 - Общий админ
        # 1 - Админ по отзывам
        # 2 - Админ по заказам
        self.manager(sql, commit=True)

    def get_admin_by_id(self, telegram_id):
        sql = '''
        SELECT * FROM admins WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def insert_admin(self, telegram_id, full_name):
        sql = '''
        INSERT INTO admins(telegram_id, full_name) VALUES (?,?)
        '''
        self.manager(sql, telegram_id, full_name, commit=True)

    def get_admins(self):
        sql = '''
            SELECT * FROM admins
        '''
        return self.manager(sql, fetchall=True)

    def create_locations_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS locations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER REFERENCES users(telegram_id),
            latitude TEXT,
            longitude TEXT
        )
        '''
        self.manager(sql, commit=True)

    def get_order(self, order_id):
        sql = '''
        SELECT * FROM orders WHERE order_id = ?
        '''
        return self.manager(sql, order_id, fetchone=True)

    def get_all_users(self):
        sql = '''
        SELECT telegram_id FROM users
        '''
        return self.manager(sql, fetchall=True)

    def change_order_status(self, order_id, status):
        sql = '''
        UPDATE orders 
        SET status = ?
        WHERE order_id = ?
        '''
        self.manager(sql, status, order_id, commit=True)

    def get_last_orders(self, telegram_id):
        sql = '''
        SELECT *
            FROM orders
            WHERE telegram_id = ?
            ORDER BY order_time DESC
            LIMIT 3;
        '''
        return self.manager(sql, telegram_id, fetchall=True)

    def get_order_products(self, order_id):
        sql = '''SELECT * FROM order_products WHERE order_id = ?'''
        return self.manager(sql, order_id, fetchall=True)

    def change_product_status(self, product_id):
        sql = '''
        UPDATE products
        SET status = 'Закончились' WHERE product_id = ?
        '''
        self.manager(sql, product_id, commit=True)

    def change_product_status1(self, product_id):
        sql = '''
        UPDATE products
        SET status = 'в наличии' WHERE product_id = ?
        '''
        self.manager(sql, product_id, commit=True)

    def create_delivery_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS delivery(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price INTEGER
        )
        '''
        self.manager(sql, commit=True)

    def create_default_price(self):
        sql = '''
        INSERT INTO delivery(price) VALUES (5000)
        '''
        self.manager(sql, commit=True)

    def update_delivery_price(self, price):
        sql = '''
        UPDATE delivery
        SET price = ? WHERE id = 1
        '''
        self.manager(sql, price, commit=True)

    def get_delivery_price(self):
        sql = '''
        SELECT price FROM delivery WHERE id = 1
        '''
        return self.manager(sql, fetchone=True)[0]

    def update_price_product(self, product_id, price):
        sql = '''
        UPDATE products
        SET price = ?
        WHERE product_id = ?
        '''
        self.manager(sql, price, product_id, commit=True)

    def update_title_ru_product(self, product_id, title_ru):
        sql = '''
        UPDATE products
        SET product_title_ru = ?
        WHERE product_id = ?
        '''
        self.manager(sql, title_ru, product_id, commit=True)

    def update_title_uz_product(self, product_id, title_uz):
        sql = '''
        UPDATE products
        SET product_title_uz = ?
        WHERE product_id = ?
        '''
        self.manager(sql, title_uz, product_id, commit=True)

    def update_desc_ru_product(self, product_id, description_ru):
        sql = '''
        UPDATE products
        SET description_ru = ?
        WHERE product_id = ?
        '''
        self.manager(sql, description_ru, product_id, commit=True)

    def update_desc_uz_product(self, product_id, description_uz):
        sql = '''
        UPDATE products
        SET description_uz = ?
        WHERE product_id = ?
        '''
        self.manager(sql, description_uz, product_id, commit=True)

    def update_photo_product(self, product_id, price):
        sql = '''
        UPDATE products
        SET image = ?
        WHERE product_id = ?
        '''
        self.manager(sql, price, product_id, commit=True)

    def get_firm_id_by_product_id(self, product_id):
        sql = '''
        SELECT firm_id FROM products WHERE product_id = ?
        '''
        return self.manager(sql, product_id, fetchone=True)[0]

    def alter_products_available(self):
        sql = 'ALTER TABLE products ADD COLUMN available INTEGER DEFAULT 1;'
        self.manager(sql, commit=True)

    def change_available(self, product_id):
        sql = '''
        UPDATE products
        SET available = CASE
            WHEN available = 1 THEN 0
            ELSE 1
        END
        WHERE product_id = ?
        '''
        self.manager(sql, product_id, commit=True)