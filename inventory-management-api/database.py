import sqlite3

DB_NAME = "inventory.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS category (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS supplier (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS product (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT NOT NULL UNIQUE,
        price REAL NOT NULL CHECK (price >= 0),
        quantity INTEGER NOT NULL CHECK (quantity >= 0),
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES category(category_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS product_detail (
        detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL UNIQUE,
        description TEXT,
        warranty_months INTEGER CHECK (warranty_months >= 0),
        FOREIGN KEY (product_id) REFERENCES product(product_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS product_supplier (
        product_id INTEGER NOT NULL,
        supplier_id INTEGER NOT NULL,
        PRIMARY KEY (product_id, supplier_id),
        FOREIGN KEY (product_id) REFERENCES product(product_id),
        FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id)
    )
    """)

    conn.commit()
    conn.close()