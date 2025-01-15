import sqlite3

DATABASE = 'database.db'

# initialise database & create tables
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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        groups TEXT NOT NULL, 
        editor TEXT NOT NULL,
        viewer TEXT NOT NULL,
        owner TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dashboards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        groups TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


# populate departments & groups only for EMPTY database file
# def populate():
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#
#     # Add initial departments
#     departments = ['Architecture', 'Commuter & Road Infrastructure (CRI)', 'Geomatics & Survey (GSV)', 'Geotechnical & Tunnels (GTT)',
#                    'Land (LD)', 'Project Management', 'Road & Rail Systems Engineering (RSE)']
#     for department in departments:
#         cursor.execute('''
#         INSERT OR IGNORE INTO departments (name)
#         VALUES (?)
#         ''', (department,))
#
#     # Add initial groups
#     groups = ['Editors_Arch', 'Editors_CRI', 'Editors_CSV', 'Editors_CTIPS', 'Editors_GTT', 'Editors_LAND',
#               'Editors_RSE', 'IDE General Viewers']
#     for group in groups:
#         cursor.execute('''
#         INSERT OR IGNORE INTO groups (name)
#         VALUES (?)
#         ''', (group,))
#
#     conn.commit()
#     conn.close()


if __name__=='__main__':
    init_db()
    # populate()