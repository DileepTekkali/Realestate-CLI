import sqlite3
from models import Property

DB_NAME = "real_estate.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL NOT NULL,
                area TEXT NOT NULL,
                property_type TEXT NOT NULL,
                contact TEXT NOT NULL,
                UNIQUE(title, area, contact)
            )
        ''')
        conn.commit()

def search_properties(area=None, max_price=None):
    query = "SELECT * FROM properties WHERE 1=1"
    params = []
    
    if area:
        query += " AND area LIKE ?"
        params.append(f"%{area}%")
    if max_price:
        query += " AND price <= ?"
        params.append(max_price)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [Property(**dict(row)) for row in rows]
