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
        viewer TEXT NOT NULL
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


# populate layers for testing
def populate_layers():
    # connect to sqlite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # define division & group
    department = 'Architecture'
    group = 'Editors_ARCH'

    # Insert 20 layers under the specified department
    try:
        for i in range(1, 21):  # Loop to create 20 layers
            layer_name = f"Layer_{i}"
            cursor.execute('''
                    INSERT INTO layers (name, department, groups) 
                    VALUES (?, ?, ?)
                ''', (layer_name, department, group))

        # Commit the changes for layers
        conn.commit()
        print("Successfully added 20 layers under 'Architecture' department.")
    except sqlite3.Error as e:
        print(f"An error occurred while adding layers: {e}")
    finally:
        # Close the database connection
        conn.close()

if __name__=='__main__':
    init_db()
    # populate()