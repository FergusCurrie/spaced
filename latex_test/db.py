import sqlite3

def create_db():
    connection = sqlite3.connect('latex_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS latex_entries (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

def insert_entry(content):
    connection = sqlite3.connect('latex_data.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO latex_entries (content) VALUES (?)', (content,))
    connection.commit()
    connection.close()

def get_entries():
    connection = sqlite3.connect('latex_data.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM latex_entries')
    entries = cursor.fetchall()
    connection.close()
    return entries


if __name__ == "__main__":
    create_db()
