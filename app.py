from flask import Flask, g, flash, request, redirect, render_template, url_for, session, jsonify
from models.Forms import LoginForm, AddLayerForm, UpdateLayerForm, AddUserForm, UpdateUserForm, AddDepartmentForm, \
    AddGroupForm, AddDashboardForm, UpdateDashboardForm
import sqlite3, requests
from arcgis.gis import GIS


app = Flask(__name__)
DATABASE = 'database.db'


# config app
app.config['SECRET_KEY'] = 'SECRET_KEY'

# ArcGIS OAuth details
# ARCGIS_CLIENT_ID = "X0HS2agHOXwNSChB"
# ARCGIS_CLIENT_SECRET = "fe22544ff4484415a0833a8c74f1136f"
# REDIRECT_URI = "http://127.0.0.1:5000/callback"
# ARCGIS_AUTH_URL = "https://ltasg.maps.arcgis.com/sharing/rest/oauth2/authorize"
# ARCGIS_TOKEN_URL = "https://ltasg.maps.arcgis.com/sharing/rest/oauth2/token"

ARCGIS_PORTAL_URL = "https://ignite.lta.gov.sg/portal/home"
ARCGIS_CLIENT_ID = "3g0BXQs78qg1a9at"
ARCGIS_CLIENT_SECRET = "e6270113788a475a8587244e8e092f8b"
REDIRECT_URI = "http://localhost:5000/callback"
ARCGIS_AUTH_URL = "https://ignite.lta.gov.sg/portal/sharing/rest/oauth2/authorize"
ARCGIS_TOKEN_URL = "https://ignite.lta.gov.sg/portal/sharing/rest/oauth2/token"

@app.route('/')
def home():
    # check if user is authenticated
    if "access_token" not in session:
        return redirect('/login')

    # if authenticated, redirect to homepage
    return render_template("homepage.html", authenticated=True)
    # return render_template("homepage.html")


@app.route('/login')
def login():
    # redirect to ArcGIS OAuth2 login page
    return redirect(f"{ARCGIS_AUTH_URL}?client_id={ARCGIS_CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}")


@app.route('/callback')
def callback():
    """Handles OAuth callback and stores token in session."""
    print(request.args)
    code = request.args.get("code")

    if code:
        token_url = ARCGIS_TOKEN_URL
        params = {
        "client_id": ARCGIS_CLIENT_ID,
        "client_secret": ARCGIS_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        }

        response = requests.post(ARCGIS_TOKEN_URL, data=params)
        token_data = response.json()

        if response.status_code == 200:
            # save the OAuth token in the session
            session['oauth_token'] = token_data['access_token']
            print('Access token received:', session['oauth_token'])
            return redirect(url_for('database'))

        else:
            return f"Error: {token_data.get('error_description', 'Unknown error')}"

    else:
        return "Error: No authorization code received"


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     login_form = LoginForm()
#     login_failed = False
#
#     if request.method == 'POST' and login_form.validate_on_submit():
#         password = login_form.password.data
#
#         if password == 'S&Lrail8':
#             session['logged_in'] = True
#             print("Login Successful!")
#
#             return redirect(url_for('home'))
#
#         else:
#             flash('Login Unsuccessful. Please try again.', 'danger')
#             login_failed = True
#
#     return render_template('login.html', form=login_form, login_failed=login_failed)


@app.route('/logout')
def logout():
    session.pop('access_token', None)
    return redirect('/')


# retrieve users on Ignite with ArcGIS Rest JS
@app.route('/get_users', methods=['GET'])
def get_users():
    # get OAuth token from session
    oauth_token = session.get('oauth_token')

    if not oauth_token:
        return "No OAuth token found. Please log in first."

    url = "https://ignite.lta.gov.sg/portal/sharing/rest/portals/self/users/search"
    params = {
            'f': 'json',
            'token': oauth_token,
            'q': '*',       # fetch all users
            'num': 100,     # max no. per request
            'start': 1,     # start at first user
        }

    all_users = []

    while True:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return f"Error retrieving users: {response.status_code} - {response.text}"

        data = response.json()
        users = data.get('results', [])
        all_users.extend(users)

        # check if there is another page
        if 'nextStart' in data and data['nextStart'] > 0:
            params['start'] = data['nextStart']     # move to next page
        else:
            break       # no more users to fetch

    count_users = len(all_users)

    return render_template('get_users.html', all_users=all_users, count_users=count_users)


# @app.route('/get_users', methods=['GET'])
# def get_users():
#     # get OAuth token from session
#     oauth_token = session.get('oauth_token')
#
#     # redirect to login if not authenticated
#     if not oauth_token:
#         return "No OAuth token found. Please log in first."
#
#     # use OAuth token to authenticate with ArcGIS
#     gis = GIS(ARCGIS_PORTAL_URL, token=oauth_token)
#     print(f"Logged in as: {gis.users.me.username}")
#
#     # search for groups
#     all_users = gis.users.search('q:*', max_users=5000)
#     print(all_users)
#
#     count_users = len(all_users)
#
#     return render_template('get_users.html', all_users=all_users, count_users=count_users)


@app.route('/get_groups', methods=['GET'])
def get_groups():
    # get OAuth token from session
    oauth_token = session.get('oauth_token')

    # redirect to login if not authenticated
    if not oauth_token:
        return "No OAuth token found. Please log in first."

    # use OAuth token to authenticate with ArcGIS
    gis = GIS(ARCGIS_PORTAL_URL, token=oauth_token)
    print(f"Logged in as: {gis.users.me.username}")

    # search for groups
    all_groups = gis.groups.search('q:*', max_groups=1000)
    print(all_groups)

    count_groups = len(all_groups)

    return render_template('get_groups.html', all_groups=all_groups, count_groups=count_groups)


# @app.route('/get_groups', methods=['GET'])
# def get_groups():
#     # get OAuth token from session
#     oauth_token = session.get('oauth_token')
#
#     if not oauth_token:
#         return "No OAuth token found. Please log in first."
#
#     url = "https://ignite.lta.gov.sg/portal/home/groups"
#     params = {
#             'f': 'json',
#             'token': oauth_token,
#             'q': '*',       # fetch all users
#             'num': 100,     # max no. per request
#             'start': 1,     # start at first user
#         }
#
#     all_groups = []
#
#     while True:
#         response = requests.get(url, params=params)
#
#         # Check and print the Content-Type header
#         print("Response Status Code:", response.status_code)
#         print("Response Content-Type:", response.headers.get('Content-Type'))
#
#         # If not JSON, return the raw content
#         if response.status_code != 200:
#             return f"Error retrieving groups: {response.status_code} - {response.text}"
#
#         if 'application/json' not in response.headers.get('Content-Type', ''):
#             return f"Expected JSON response but got: {response.headers.get('Content-Type')}\n{response.text}"
#
#         try:
#             data = response.json()
#         except requests.exceptions.JSONDecodeError:
#             return f"Error decoding JSON: {response.text}"
#
#         groups = data.get('results', [])
#         all_groups.extend(groups)
#
#         # Check if there is another page
#         if 'nextStart' in data and data['nextStart'] > 0:
#             params['start'] = data['nextStart']
#         else:
#             break  # No more groups to fetch
#
#     count_groups = len(all_groups)
#
#     return render_template('get_groups.html', all_groups=all_groups, count_groups=count_groups)


def recalculate_user_permissions(cursor, user):
    # extract user details
    user_id, name, department, groups, editor, viewer, owner = user
    user_groups = set(groups.split(', '))

    # fetch all layers & dashboards
    cursor.execute('SELECT name, groups FROM layers')
    layers = cursor.fetchall()
    cursor.execute('SELECT name, groups FROM dashboards')
    dashboards = cursor.fetchall()

    # initialise permissions
    updated_editor_layers = set()
    updated_viewer_layers = set()
    updated_owner_dashboards = set()

    # process layer permissions
    for layer_name, layer_groups in layers:
        layer_groups_set = set(group.strip() for group in layer_groups.split(', '))
        overlap = user_groups.intersection(layer_groups_set)

        if overlap:
            if overlap == {'IDE - General Viewers'}:
                updated_viewer_layers.add(layer_name)
            elif len(overlap) > 1 or not {'IDE - General Viewers'}.issubset(overlap):
                updated_editor_layers.add(layer_name)
                updated_viewer_layers.add(layer_name)

    # Process dashboard permissions
    for dashboard_name, dashboard_group in dashboards:
        dashboard_group_set = set(group.strip() for group in dashboard_group.split(', '))
        overlap = user_groups.intersection(dashboard_group_set)

        if overlap:
            updated_viewer_layers.add(dashboard_name)

    # Convert to comma-separated strings
    updated_editor = ', '.join(updated_editor_layers)
    updated_viewer = ', '.join(updated_viewer_layers)

    # Update the user's permissions in the database
    cursor.execute('''
        UPDATE users
        SET editor = ?, viewer = ?
        WHERE id = ?
        ''', (updated_editor, updated_viewer, user_id))


@app.route('/add_layer', methods=['POST', 'GET'])
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

            # recalculate permissions for all users
            cursor.execute('SELECT * FROM users')
            all_users = cursor.fetchall()
            for user in all_users:
                recalculate_user_permissions(cursor, user)

            conn.commit()

            print('update user permissions after adding layer!')
            return redirect(url_for('all_layers'))

        except sqlite3.Error as e:
            print(f"An error: {e}")

    conn.close()
    return render_template('add_layer.html', form=add_layer_form)


@app.route('/update_layer/<int:layer_id>', methods=['POST', 'GET'])
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

            # recalculate permissions for all users
            cursor.execute('SELECT * FROM users')
            all_users = cursor.fetchall()
            for user in all_users:
                recalculate_user_permissions(cursor, user)

            conn.commit()

            print('update user permissions after updating layer!')
            return redirect(url_for('all_layers'))

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    conn.close()
    return render_template('update_layer.html', form=update_layer_form, layer_data=layer_data)


@app.route('/delete_layer/<int:layer_id>', methods=['POST', 'GET'])
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
        # if "All Departments" is selected or no filter is applied, fetch ALL layers
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

    # fetch layers
    cursor.execute('SELECT name, groups FROM layers')
    layers = cursor.fetchall()

    # fetch dashboards
    cursor.execute('SELECT name, groups FROM dashboards')
    dashboards = cursor.fetchall()

    # fetch layers & group them by groups
    cursor.execute('SELECT name, groups FROM layers')
    layers_by_group = {}
    for layer_name, group in cursor.fetchall():
        if group not in layers_by_group:
            layers_by_group[group] = []
        layers_by_group[group].append(layer_name)

    # flatten all layers
    all_layers = [layer for layers in layers_by_group.values() for layer in layers]

    # populate form with existing choices
    add_user_form.department.choices = [(dept, dept) for dept in departments]
    add_user_form.groups.choices = [(grp, grp) for grp in groups]
    add_user_form.dashboards.choices = [(dashboard[0], dashboard[0]) for dashboard in dashboards]

    # process form submission
    if request.method == 'POST' and add_user_form.validate_on_submit():
        name = add_user_form.name.data
        departments = add_user_form.department.data
        user_groups = set(add_user_form.groups.data)
        selected_dashboards = set(add_user_form.dashboards.data)

        # check if user already exists ( duplicate users not allowed )
        cursor.execute('SELECT COUNT(*) FROM users WHERE name = ?', (name,))
        if cursor.fetchone()[0] > 0:
            flash(f"User '{name}' already exists!", 'danger')
            print('user already exists')
            return render_template('add_user.html', form=add_user_form, layers_by_group=layers_by_group, user_exists=True)

        # initialize permissions for layers
        editor = []
        viewer = []
        owner = []

        # Debug: Print the user_groups
        print(f"User Groups: {user_groups}")

        # process the permissions for each layer
        for layer_name, layer_groups in layers:
            # Convert the layer groups to a set for comparison
            layer_groups_set = set(group.strip() for group in layer_groups.split(', '))  # Remove leading/trailing spaces
            overlap = user_groups.intersection(layer_groups_set)

            # Print the overlap for this layer
            print(f"Layer: {layer_name} | Layer Groups: {layer_groups_set} | Overlap: {overlap}")

            # handle permissions logic here
            if overlap:
                if len(overlap) == 1 and 'IDE - General Viewers' in overlap:
                    viewer.append(layer_name)
                elif len(overlap) > 1 or not {'IDE - General Viewers'}.issubset(overlap):
                    editor.append(layer_name)
                    viewer.append(layer_name)

        # process the permissions for each dashboard
        for dashboard_name, dashboard_group in dashboards:
            dashboard_group_set = set(group.strip() for group in dashboard_group.split(', '))
            overlap = user_groups.intersection(dashboard_group_set)

            if dashboard_name in selected_dashboards:
                print(f"Adding {dashboard_name} to owner")
                owner.append(dashboard_name)
                continue

            if overlap:
                print(f"Adding {dashboard_name} to viewer")
                viewer.append(dashboard_name)

        # convert lists into comma-separated strings
        department_string = ', '.join(departments)
        group_string = ', '.join(user_groups)
        editor_string = ', '.join(editor)
        viewer_string = ', '.join(viewer)
        owner_string = ', '.join(owner)

        # insert into SQLite database
        try:
            # insert new user into users table
            cursor.execute('''
                    INSERT INTO users (name, department, groups, editor, viewer, owner)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                name, department_string, group_string, editor_string, viewer_string, owner_string))

            conn.commit()

            print('User added successfully!')
            return redirect(url_for('all_users'))

        except sqlite3.Error as e:
            print(f"An error: {e}")
            return render_template('add_user.html', form=add_user_form)

    conn.close()
    return render_template('add_user.html', form=add_user_form, layers_by_group=layers_by_group)


@app.route('/update_user/<int:user_id>', methods=['POST', 'GET'])
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

    # fetch dashboards
    cursor.execute('SELECT name, groups FROM dashboards')
    dashboards = cursor.fetchall()

    # fetch layers & group them by groups
    cursor.execute('SELECT name, groups FROM layers')
    layers = cursor.fetchall()
    layers_by_group = {}
    for layer_name, group in layers:
        if group not in layers_by_group:
            layers_by_group[group] = []
        layers_by_group[group].append(layer_name)

    # Flatten all layers
    all_layers = [layer for layers in layers_by_group.values() for layer in layers]

    # initialize the update user form
    update_user_form = UpdateUserForm(
        name=user_data[1],
        department=user_data[2].split(', '),
        groups=user_data[3].split(', '),
        editor=user_data[4].split(', '),
        viewer=user_data[5].split(', '),
        dashboards=user_data[6].split(', '))

    # populate form fields
    update_user_form.department.choices = [(dept, dept) for dept in departments]
    update_user_form.groups.choices = [(grp, grp) for grp in groups]
    update_user_form.editor.choices = [(layer, layer) for layer in all_layers]
    update_user_form.viewer.choices = [(layer, layer) for layer in all_layers]
    update_user_form.dashboards.choices = [(dashboard[0], dashboard[0]) for dashboard in dashboards]

    # process form submission
    if request.method == 'POST' and update_user_form.validate_on_submit():
        updated_name = update_user_form.name.data
        updated_department = update_user_form.department.data
        updated_groups = set(update_user_form.groups.data)
        explicit_editor_layers = set(update_user_form.editor.data)
        explicit_viewer_layers = set(update_user_form.viewer.data)
        selected_dashboards = set(update_user_form.dashboards.data)

        # update permissions dynamically for layers
        updated_editor_layers = set()
        updated_viewer_layers = set()
        updated_owner_dashboards = set()

        # Debug: Print the user_groups
        print(f"User Groups: {updated_groups}")

        for layer_name, layer_groups in layers:
            layer_groups_set = set(group.strip() for group in layer_groups.split(', '))  # Strip spaces
            overlap = updated_groups.intersection(layer_groups_set)

            # Print the overlap for this layer
            print(f"Layer: {layer_name} | Layer Groups: {layer_groups_set} | Overlap: {overlap}")

            # Permissions logic
            if overlap:
                if overlap == {'IDE - General Viewers'}:
                    updated_viewer_layers.add(layer_name)  # Add to viewer list
                elif len(overlap) > 1 or not {'IDE - General Viewers'}.issubset(overlap):
                    updated_editor_layers.add(layer_name)  # Add to editor list
                    updated_viewer_layers.add(layer_name)

        # process the permissions for each dashboard
        for dashboard_name, dashboard_group in dashboards:
            dashboard_group_set = set(group.strip() for group in dashboard_group.split(', '))
            overlap = updated_groups.intersection(dashboard_group_set)

            if dashboard_name in selected_dashboards:
                print(f"Adding {dashboard_name} to owner")
                updated_owner_dashboards.add(dashboard_name)
                continue

            if overlap:
                print(f"Adding {dashboard_name} to viewer")
                updated_viewer_layers.add(dashboard_name)

        # Convert to comma-separated strings for database storage
        updated_editor = ', '.join(updated_editor_layers)
        updated_viewer = ', '.join(updated_viewer_layers)
        updated_department = ', '.join(updated_department)
        updated_group = ', '.join(updated_groups)
        updated_owner = ', '.join(updated_owner_dashboards)

        # update SQLite database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE users
            SET name = ?, department = ?, groups = ?, editor = ?, viewer = ?, owner = ?
            WHERE id = ?
            ''', (
                updated_name, updated_department, updated_group, updated_editor, updated_viewer, updated_owner,
                user_id))

            conn.commit()
            return redirect(url_for('all_users'))

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    conn.close()
    return render_template('update_user.html', form=update_user_form, user_data=user_data, user_id=user_id)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
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
def add_dashboard():
    add_dashboard_form = AddDashboardForm()

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
    add_dashboard_form.department.choices = [(dept, dept) for dept in departments]
    add_dashboard_form.groups.choices = [(grp, grp) for grp in groups]

    if request.method == 'POST' and add_dashboard_form.validate_on_submit():
        # process the form data
        name = add_dashboard_form.name.data
        departments = add_dashboard_form.department.data
        groups = add_dashboard_form.groups.data

         # automatically add '*' prefix to the dashboard name
        if not name.startswith('*'):
            name = f'*{name}'

        # convert lists into comma-separated strings
        department_string = ', '.join(departments)
        group_string = ', '.join(groups)

        # insert into SQLite database
        try:
            cursor.execute('''
                    INSERT INTO dashboards (name, department, groups)
                    VALUES (?, ?, ?)
                    ''', (name, department_string, group_string))

            conn.commit()

            print('Dashboard added successfully!')
            return redirect(url_for('all_dashboards'))

        except sqlite3.Error as e:
            print(f"An error: {e}")

    conn.close()
    return render_template('add_dashboard.html', form=add_dashboard_form)


@app.route('/update_dashboard/<int:dashboard_id>', methods=['POST', 'GET'])
def update_dashboard(dashboard_id):
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch dashboards
    cursor.execute('SELECT * FROM dashboards WHERE id = ?',
                   (dashboard_id,))
    dashboard_data = cursor.fetchone()

    if not dashboard_data:
        print("Dashboard not found!")
        return redirect(url_for('all_dashboards'))

    # fetch departments
    cursor.execute('SELECT name FROM departments')
    departments = [row[0] for row in cursor.fetchall()]

    # fetch groups
    cursor.execute('SELECT name FROM groups')
    groups = [row[0] for row in cursor.fetchall()]

    # initialize the update dashboard form
    update_dashboard_form = UpdateDashboardForm(name=dashboard_data[1], department=dashboard_data[2].split(', '),
                                        groups=dashboard_data[3].split(', '))

    # update form fields
    update_dashboard_form.department.choices = [(dept, dept) for dept in departments]
    update_dashboard_form.groups.choices = [(grp, grp) for grp in groups]

    # process form submission
    if request.method == 'POST' and update_dashboard_form.validate_on_submit():
        updated_name = update_dashboard_form.name.data
        updated_department = update_dashboard_form.department.data
        updated_groups = update_dashboard_form.groups.data

        # automatically add '*' prefix to the dashboard name
        if not updated_name.startswith('*'):
            updated_name = f'*{updated_name}'

        # convert lists into comma-separated strings
        department_string = ', '.join(updated_department)
        group_string = ', '.join(updated_groups)

        # update sqlite database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
                                UPDATE dashboards
                                SET name = ?, department = ?, groups = ?
                                WHERE id = ?
                            ''', (updated_name, department_string, group_string, dashboard_id,))
            conn.commit()

            return redirect(url_for('all_dashboards'))

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    conn.close()
    return render_template('update_dashboard.html', form=update_dashboard_form, dashboard_data=dashboard_data)


@app.route('/delete_dashboard/<int:dashboard_id>', methods=['POST', 'GET'])
def delete_dashboard(dashboard_id):
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # delete selected layer
    if request.method == 'POST':
        try:
            cursor.execute('''
                            DELETE FROM dashboards WHERE id = ?
                            ''', (dashboard_id,))
            conn.commit()
            print("Dashboard deleted successfully!")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    conn.close()
    return redirect(url_for('all_dashboards'))


@app.route('/dashboards', methods=['GET'])
def all_dashboards():
    # connect to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch search query (if any)
    search_query = request.args.get('query', '').strip()

    # fetch relevant dashboards based on search query
    if search_query:
        cursor.execute('SELECT * FROM dashboards WHERE name LIKE ? ORDER BY name ASC', (f"%{search_query}%",))
    else:
        cursor.execute('SELECT * FROM dashboards ORDER BY name ASC')
    rows = cursor.fetchall()

    conn.close()
    return render_template('dashboards.html', dashboards=rows, query=search_query)


@app.route('/database', methods=['GET'])
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

    # fetch all dashboards
    cursor.execute('SELECT name, department, groups FROM dashboards')
    dashboards = cursor.fetchall()

    # fetch all departments
    cursor.execute('SELECT name FROM departments')
    departments = [dept[0] for dept in cursor.fetchall()]

    # group layers under their respective department
    grouped_layers = {dept: [] for dept in departments}
    for layer in layers:
        department = layer[1]
        if department in grouped_layers:
            grouped_layers[department].append(layer[0])

    # group dashboards under their respective department
    grouped_dashboards = {dept: [] for dept in departments}
    for dashboard in dashboards:
        department = dashboard [1]
        if department in grouped_dashboards:
            grouped_dashboards[department].append(dashboard[0])

    # combine dashboards & layers, ensuring dashboards come first
    grouped_items = {}
    for department in departments:
        dashboards = grouped_dashboards.get(department, [])
        layers = grouped_layers.get(department, [])
        grouped_items[department] = dashboards + layers

    # calculate column spans under each department dynamically
    column_spans = {
        dept: max(len(grouped_items.get(dept, [])), 1) for dept in departments
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
            'owner': user[6].split(', '),
        })

    conn.close()
    return render_template('database.html', users=split_users, layers=layers,
                           grouped_layers=grouped_layers, grouped_items=grouped_items,
                           departments=departments, total_column_spans=total_column_spans, query=search_query)


@app.route('/add_department_group', methods=['POST', 'GET'])
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
                        ''', (department_id,))

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
                        ''', (group_id,))

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
