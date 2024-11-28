import sqlite3

DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS layers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        groups TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


# def populate_test_data():
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.executemany('''
#     INSERT INTO layers (name, department, groups)
#     VALUES (?, ?, ?)
#     ''', [
#         ('Alice', 'Engineering', 'Group A'),
#         ('Bob', 'Marketing', 'Group B'),
#         ('Charlie', 'Finance', 'Group C')
#     ])
#     conn.commit()
#     conn.close()


if __name__=='__main__':
    init_db()
    # populate_data()