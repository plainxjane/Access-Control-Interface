from flask import Flask, g, flash, request, redirect, render_template, url_for, session, jsonify
from models.Forms import LoginForm, AddLayerForm, UpdateLayerForm, AddUserForm, UpdateUserForm, AddDepartmentForm, \
    AddGroupForm
from wrappers import login_required
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# config app
app.config['SECRET_KEY'] = 'SECRET_KEY'


@app.route('/')
@login_required
def home():
    return render_template('homepage.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        password = login_form.password.data
        if password == 'S&Lrail8':
            session['logged_in'] = True
            print("Login Successful!")

            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please try again.', 'danger')

    return render_template('login.html', form=login_form)


@app.route('/logout')
@login_required
def logout():
    # remove login state
    session.pop('logged_in', None)
    flash("You have been logged out.", 'info')
    print("Logged out!")

    return redirect(url_for('login'))


@app.route('/add_layer', methods=['POST', 'GET'])
@login_required
def add_layer():
    add_layer_form = AddLayerForm()

    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch departments
    cursor.execute('SELECT name FROM departments')
    departments = [row[0] for row in cursor.fetchall()]

    # fetch groups
    cursor.execute('SELECT name FROM groups')
    groups = [row[0] for row in cursor.fetchall()]

    # populate form fields
    add_layer_form.department.choices = [(dept, dept) for dept in departments]
    add_layer_form.groups.choices = [(grp, grp) for grp in groups]

    if request.method == 'POST' and add_layer_form.validate_on_submit():
        # process the form data
        name = add_layer_form.name.data
        departments = add_layer_form.department.data
        groups = add_layer_form.groups.data

        # convert lists into comma-separated strings
        department_string = ', '.join(departments)
        group_string = ', '.join(groups)

        # insert into SQLite database
        try:
            cursor.execute('''
            INSERT INTO layers (name, department, groups)
            VALUES (?, ?, ?)
            ''', (name, department_string, group_string))

            conn.commit()

            print('Layer added successfully!')
            return redirect(url_for('all_layers'))

        except sqlite3.Error as e:
            print(f"An error: {e}")

    conn.close()
    return render_template('add_layer.html', form=add_layer_form)


@app.route('/update_layer/<int:layer_id>', methods=['POST', 'GET'])
@login_required
def update_layer(layer_id):
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch layers
    cursor.execute('SELECT * FROM layers WHERE id = ?',
                   (layer_id,))
    layer_data = cursor.fetchone()

    if not layer_data:
        print("Layer not found!")
        return redirect(url_for('all_layers'))

    # fetch departments
    cursor.execute('SELECT name FROM departments')
    departments = [row[0] for row in cursor.fetchall()]

    # fetch groups
    cursor.execute('SELECT name FROM groups')
    groups = [row[0] for row in cursor.fetchall()]

    # initialize the update layer form
    update_layer_form = UpdateLayerForm(name=layer_data[1], department=layer_data[2].split(', '),
                                        groups=layer_data[3].split(', '))

    # update form fields
    update_layer_form.department.choices = [(dept, dept) for dept in departments]
    update_layer_form.groups.choices = [(grp, grp) for grp in groups]

    # process form submission
    if request.method == 'POST' and update_layer_form.validate_on_submit():
        updated_name = update_layer_form.name.data
        updated_department = update_layer_form.department.data
        updated_groups = update_layer_form.groups.data

        # convert lists into comma-separated strings
        department_string = ', '.join(updated_department)
        group_string = ', '.join(updated_groups)

        # update sqlite database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                        UPDATE layers
                        SET name = ?, department = ?, groups = ?
                        WHERE id = ?
                    ''', (updated_name, department_string, group_string, layer_id,))
            conn.commit()

            return redirect(url_for('all_layers'))

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    conn.close()
    return render_template('update_layer.html', form=update_layer_form, layer_data=layer_data)


@app.route('/delete_layer/<int:layer_id>', methods=['POST', 'GET'])
@login_required
def delete_layer(layer_id):
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # delete selected layer
    if request.method == 'POST':
        try:
            cursor.execute('''
                        DELETE FROM layers WHERE id = ?
                        ''', (layer_id,))
            conn.commit()
            print("Layer deleted successfully!")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    conn.close()
    return redirect(url_for('all_layers'))


@app.route('/layers', methods=['GET'])
@login_required
def all_layers():
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch all distinct departments
    cursor.execute('SELECT DISTINCT name FROM departments')
    departments = [row[0] for row in cursor.fetchall()]

    # get selected departments
    selected_departments = request.args.getlist('departments[]')

    # fetch layers based on selected departments
    if 'all' in selected_departments or not selected_departments:
        # if "All Departments' is selected or no filter is applied, fetch ALL layers
        cursor.execute('SELECT * FROM layers ORDER BY name ASC')
    else:
        # if specific departments are selected, filter layers by those departments
        placeholders = ', '.join('?' for _ in selected_departments)
        query = f'SELECT * FROM layers WHERE department IN ({placeholders}) ORDER BY name ASC'
        cursor.execute(query, selected_departments)

    rows = cursor.fetchall()

    conn.close()
    return render_template('layers.html', rows=rows, departments=departments, selected_departments=selected_departments)


@app.route('/add_user', methods=['POST', 'GET'])
@login_required
def add_user():
    add_user_form = AddUserForm()

    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch departments
    cursor.execute('SELECT name FROM departments')
    departments = [row[0] for row in cursor.fetchall()]

    # fetch groups
    cursor.execute('SELECT name FROM groups')
    groups = [row[0] for row in cursor.fetchall()]

    # fetch layers & group them by department
    cursor.execute('SELECT name, department FROM layers')
    layers_by_department = {}
    for layer_name, department in cursor.fetchall():
        if department not in layers_by_department:
            layers_by_department[department] = []
        layers_by_department[department].append(layer_name)

    # flatten all layers
    all_layers = [layer for layers in layers_by_department.values() for layer in layers]

    # populate form with existing choices
    add_user_form.department.choices = [(dept, dept) for dept in departments]
    add_user_form.groups.choices = [(grp, grp) for grp in groups]
    add_user_form.editor.choices = [(layer, layer) for layer in all_layers]
    add_user_form.viewer.choices = [(layer, layer) for layer in all_layers]

    # process form submission
    if request.method == 'POST' and add_user_form.validate_on_submit():
        name = add_user_form.name.data
        departments = add_user_form.department.data
        groups = add_user_form.groups.data
        editor = add_user_form.editor.data
        viewer = add_user_form.viewer.data

        # check if user belongs to the 'IDE - General Viewers' group
        if 'IDE - General Viewers' in groups:
            # if so, assign all layers to viewer field
            viewer = all_layers

        # if departments are selected, assign layers to both viewer & editor based on those departments
        selected_layers = set()
        for dept in departments:
            selected_layers.update(layers_by_department.get(dept, []))

        editor.extend(selected_layers)
        viewer.extend(selected_layers)

        # convert lists into comma-separated strings
        department_string = ', '.join(departments)
        group_string = ', '.join(groups)
        editor_string = ', '.join(editor)
        viewer_string = ', '.join(viewer)

        # insert into SQLite database
        try:
            # insert new user into users table
            cursor.execute('''
                    INSERT INTO users (name, department, groups, editor, viewer)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                name, department_string, group_string, editor_string, viewer_string))

            conn.commit()

            print('User added successfully!')
            return redirect(url_for('all_users'))

        except sqlite3.Error as e:
            print(f"An error: {e}")
            return render_template('add_user.html', form=add_user_form)

    conn.close()
    return render_template('add_user.html', form=add_user_form, layers_by_department=layers_by_department)


@app.route('/update_user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def update_user(user_id):
    # fetch user's data from database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?',
                   (user_id,))
    user_data = cursor.fetchone()

    if not user_data:
        print("User not found!")
        return redirect(url_for('all_users'))

    # fetch departments
    cursor.execute('SELECT name FROM departments')
    departments = [row[0] for row in cursor.fetchall()]

    # fetch groups
    cursor.execute('SELECT name FROM groups')
    groups = [row[0] for row in cursor.fetchall()]

    # fetch layers & group them by department
    cursor.execute('SELECT name, department FROM layers')
    layers_by_department = {}
    for layer_name, department in cursor.fetchall():
        if department not in layers_by_department:
            layers_by_department[department] = []
        layers_by_department[department].append(layer_name)

    # flatten all layers
    all_layers = [layer for layers in layers_by_department.values() for layer in layers]

    # initialize the update user form
    update_user_form = UpdateUserForm(name=user_data[1], department=user_data[2].split(', '),
                                      groups=user_data[3].split(', '), editor=user_data[4].split(', '),
                                      viewer=user_data[5].split(', '))

    # populate form fields
    update_user_form.department.choices = [(dept, dept) for dept in departments]
    update_user_form.groups.choices = [(grp, grp) for grp in groups]
    update_user_form.editor.choices = [(layer, layer) for layer in all_layers]
    update_user_form.viewer.choices = [(layer, layer) for layer in all_layers]

    # process form submission
    if request.method == 'POST' and update_user_form.validate_on_submit():
        updated_name = update_user_form.name.data
        updated_department = update_user_form.department.data
        updated_groups = update_user_form.groups.data

        # fetch current departments from the database
        current_departments = user_data[2].split(', ')

        print(updated_groups)

        # check if user is in 'ide - general viewers' group
        is_in_general_viewers = 'IDE - General Viewers' in updated_groups

        # determine layers to remove (layers from previous departments not in the new departments)
        layers_to_remove = set()
        if not is_in_general_viewers:
            for dept in current_departments:
                if dept not in updated_department:
                    layers_to_remove.update(layers_by_department.get(dept, []))

        # determine layers to add (layers from new departments not in the old departments)
        layers_to_add = set()
        for dept in updated_department:
            if dept not in current_departments:
                layers_to_add.update(layers_by_department.get(dept, []))

        # Fetch current editor and viewer layers
        current_editor_layers = set(user_data[4].split(', '))
        current_viewer_layers = set(user_data[5].split(', '))

        # Update editor layers
        updated_editor_layers = (current_editor_layers - layers_to_remove).union(layers_to_add)

        # update viewer layers
        if is_in_general_viewers:
            updated_viewer_layers = set(all_layers)
        else:
            updated_viewer_layers = (current_viewer_layers - layers_to_remove).union(layers_to_add)

        print(updated_editor_layers)
        print(updated_viewer_layers)

        # Convert to comma-separated strings for database storage
        updated_editor = ', '.join(updated_editor_layers)
        updated_viewer = ', '.join(updated_viewer_layers)
        updated_department = ', '.join(updated_department)
        updated_group = ', '.join(updated_groups)

        # update SQLite database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE users
            SET name = ?, department = ?, groups = ?, editor = ?, viewer = ?
            WHERE id = ?
            ''', (
                updated_name, updated_department, updated_group, updated_editor, updated_viewer,
                user_id))

            conn.commit()
            return redirect(url_for('all_users'))

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    conn.close()
    return render_template('update_user.html', form=update_user_form, user_data=user_data, user_id=user_id)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # delete selected user
    if request.method == 'POST':
        try:
            cursor.execute('''
                            DELETE FROM users WHERE id = ?
                            ''', (user_id,))
            conn.commit()
            print("User deleted successfully!")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    conn.close()
    return redirect(url_for('all_users'))


@app.route('/users', methods=['GET'])
@login_required
def all_users():
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch search query (if any)
    search_query = request.args.get('query', '').strip()

    # fetch relevant users based on search query
    if search_query:
        cursor.execute('SELECT * FROM users WHERE name LIKE ? ORDER BY name ASC', (f"%{search_query}%",))
    else:
        cursor.execute('SELECT * FROM users ORDER BY name ASC')
    users = cursor.fetchall()

    # fetch layers
    cursor.execute('SELECT name, department FROM layers')
    layers = cursor.fetchall()

    # fetch departments
    cursor.execute('SELECT name FROM departments')
    departments = [dept[0] for dept in cursor.fetchall()]

    # group layers by department
    grouped_layers = {dept: [] for dept in departments}
    for layer in layers:
        department = layer[1]
        if department in grouped_layers:
            grouped_layers[department].append(layer[0])

    # calculate the length of col-span dynamically
    column_spans = {
        dept: max(len(grouped_layers.get(dept, [])), 1) for dept in departments
    }
    total_column_spans = sum(column_spans.values())

    # split user fields before passing into template
    split_users = []
    for user in users:
        split_users.append({
            'id': user[0],
            'name': user[1],
            'department': user[2].split(', '),
            'groups': user[3].split(', '),
            'editor': user[4].split(', '),
            'viewer': user[5].split(', '),
        })

    conn.close()
    return render_template('users.html', users=split_users, layers=layers, grouped_layers=grouped_layers,
                           departments=departments, total_column_spans=total_column_spans, query=search_query)


@app.route('/add_dashboard', methods=['POST', 'GET'])
@login_required
def add_dashboard():
    pass


@app.route('/update_dashboard', methods=['POST', 'GET'])
@login_required
def update_dashboard():
    pass


@app.route('/delete_dashboard', methods=['POST'])
@login_required
def delete_dashboard():
    pass


@app.route('/dashboards')
@login_required
def all_dashboards():
    pass


@app.route('/database', methods=['GET'])
@login_required
def database():
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch search query (if any)
    search_query = request.args.get('query', '').strip()

    # fetch relevant users based on search query
    if search_query:
        cursor.execute('SELECT * FROM users WHERE name LIKE ?', (f"%{search_query}%",))
    # fetch all users if no search query
    else:
        cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    # fetch all layers
    cursor.execute('SELECT name, department, groups FROM layers')
    layers = cursor.fetchall()

    # fetch all departments
    cursor.execute('SELECT name FROM departments')
    departments = [dept[0] for dept in cursor.fetchall()]

    # group layers under their respective department
    grouped_layers = {dept: [] for dept in departments}
    for layer in layers:
        department = layer[1]
        if department in grouped_layers:
            grouped_layers[department].append(layer[0])

    # calculate column spans under each department dynamically
    column_spans = {
        dept: max(len(grouped_layers.get(dept, [])), 1) for dept in departments
    }
    total_column_spans = sum(column_spans.values())

    # split user fields before passing to template
    split_users = []
    for user in users:
        split_users.append({
            'id': user[0],
            'name': user[1],
            'department': user[2].split(', '),
            'groups': user[3].split(', '),
            'editor': user[4].split(', '),
            'viewer': user[5].split(', '),
        })

    conn.close()
    return render_template('database.html', users=split_users, layers=layers,
                           grouped_layers=grouped_layers,
                           departments=departments, total_column_spans=total_column_spans, query=search_query)


@app.route('/add_department_group', methods=['POST', 'GET'])
@login_required
def add_department_group():
    # connect to sqlite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch existing departments
    cursor.execute('SELECT * FROM departments')
    departments = cursor.fetchall()

    # fetch existing groups
    cursor.execute('SELECT * FROM groups')
    groups = cursor.fetchall()

    # initialise add department/group forms
    add_department_form = AddDepartmentForm()
    add_group_form = AddGroupForm()

    if request.method == 'POST':
        # process the 'Add Department' request
        if add_department_form.validate_on_submit() and 'add_department' in request.form:
            department_name = add_department_form.name.data

            # insert into Departments table in SQLite database
            try:
                cursor.execute('''
                            INSERT INTO departments (name) VALUES (?)
                            ''', (department_name,))

                conn.commit()
                return redirect(url_for('add_department_group'))

            except sqlite3.Error as e:
                print(f"An error has occurred: {e}")

        # process the 'Add Group' request
        elif add_group_form.validate_on_submit() and 'add_group' in request.form:
            group_name = add_group_form.name.data

            # insert into Groups table in SQLite database
            try:
                cursor.execute('''
                            INSERT INTO groups (name) VALUES (?)
                            ''', (group_name,))

                conn.commit()
                return redirect(url_for('add_department_group'))

            except sqlite3.Error as e:
                print(f"An error has occurred {e}")

        # process the 'Delete Department' request
        elif 'delete_department' in request.form:
            department_id = request.form.get('delete_department')

            # delete from Departments table in SQLite database
            try:
                cursor.execute('''
                        DELETE FROM departments WHERE id = ?
                        ''', (department_id, ))

                conn.commit()
                return redirect(url_for('add_department_group'))

            except sqlite3.Error as e:
                print(f"An error has occurred: {e}")

        # process the 'Delete Group' request
        elif 'delete_group' in request.form:
            group_id = request.form.get('delete_group')

            # delete from Groups table in SQLite database
            try:
                cursor.execute('''
                            DELETE FROM groups WHERE id = ?
                        ''', (group_id, ))

                conn.commit()
                return redirect(url_for('add_department_group'))

            except sqlite3.Error as e:
                print(f"An error has occurred: {e}")

    conn.close()
    return render_template('add_department_group.html', departments=departments, groups=groups,
                               add_department_form=add_department_form,
                               add_group_form=add_group_form)


if __name__ == '__main__':
    app.run(debug=True)
