from config import DB_NAME, DB_PASSWORD, DB_USER, DB_HOST
import psycopg2


class DataBase:
    def __init__(self):
        self.database = psycopg2.connect(
            database=DB_NAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            user=DB_USER
        )

    def manager(self, sql, *args,
                commit: bool = False,
                fetchone: bool = False,
                fetchall: bool = False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    return db.commit()
                elif fetchall:
                    return cursor.fetchall()
                elif fetchone:
                    return cursor.fetchone()

    def create_table_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(60),
            contact VARCHAR(15) UNIQUE,
            birthdate DATE
        )'''
        self.manager(sql, commit=True)

    def insert_telegram_id_user(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id)
        VALUES(%s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, (telegram_id,), commit=True)

    def check_user_info(self, telegram_id):
        sql = '''SELECT * FROM users
        WHERE telegram_id = %s'''
        return self.manager(sql, telegram_id, fetchone=True)

    def update_user_info(self, full_name, contact, birthdate, telegram_id):
        sql = '''UPDATE users SET full_name = %s,
        contact = %s, birthdate = %s WHERE telegram_id = %s'''
        self.manager(sql, full_name, contact, birthdate, telegram_id, commit=True)

    def create_table_categories(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(60) UNIQUE
        )'''
        self.manager(sql, commit=True)

    def create_table_products(self):
        sql = '''CREATE TABLE IF NOT EXISTS products(
            product_id SERIAL PRIMARY KEY,
            product_name TEXT UNIQUE,
            price BIGINT,
            image TEXT,
            link TEXT,
            category_id INTEGER REFERENCES categories(category_id)
        )'''
        self.manager(sql, commit=True)

    def select_category_id_by_cat_name(self, category):
        sql = '''SELECT category_id FROM categories
        WHERE category_name = %s'''
        return self.manager(sql, category, fetchone=True)

    def insert_category_name(self, category):
        sql = '''INSERT INTO categories(category_name)
        VALUES(%s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, (category,), commit=True)

    def insert_product_to_products(self, product_name, price, image, link, category_id):
        sql = '''INSERT INTO products(product_name, price, image, link, category_id)
        VALUES(%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, product_name, price, image, link, category_id, commit=True)

    def get_all_categories(self):
        sql = '''SELECT category_name FROM categories'''
        return self.manager(sql, fetchall=True)


    def get_product_by_pagination(self, category_name, offset, limit):
        sql = '''SELECT * FROM products
        WHERE category_id = (select category_id from categories where category_name = %s)
        OFFSET %s
        LIMIT %s'''
        return self.manager(sql, category_name, offset, limit, fetchall=True)


    def count_of_product(self, category_name):
        sql = '''SELECT count(product_id) FROM products
        WHERE category_id = (select category_id from categories where category_name = %s)'''
        return self.manager(sql, category_name, fetchone=True)[0]


    def get_product_info(self, product_id):
        sql = '''SELECT * FROM products
        WHERE product_id = %s'''
        return self.manager(sql, product_id, fetchone=True)

    def get_category_name_by_category_id(self, category_id):
        sql = '''SELECT category_name FROM categories
        WHERE category_id = %s'''
        return self.manager(sql, category_id, fetchone=True)[0]
