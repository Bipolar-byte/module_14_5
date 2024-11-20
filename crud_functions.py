import sqlite3

DB_NAME = "products.db"


def initiate_db():
    """Создает таблицы Products и Users, если они еще не существуют."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_user(username, email, age):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)
    """, (username, email, age, 1000))
    conn.commit()
    conn.close()


def is_included(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, price FROM Products")
    products = cursor.fetchall()
    conn.close()
    return products


def add_test_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO Products (title, description, price) VALUES (?, ?, ?)
    """, [
        ("Product1", "Ножи ручной работы", 100),
        ("Product2", "Охотничий нож GIKO", 200),
        ("Product3", "Нож керамбит", 300),
        ("Product4", "Нож Катран", 400),
    ])
    conn.commit()
    conn.close()
