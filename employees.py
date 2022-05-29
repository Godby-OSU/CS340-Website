from flask import  render_template, redirect, request, Blueprint
from app import mysql as mysql

# ----------------------------------------------------------------
# Creating Blueprints
    # Citation for the following methods: Creating Blueprint and labeling routes
    # Date: 5/23/2022
    # Adapted from:
    # Source URL: https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
# ----------------------------------------------------------------
create_employees = Blueprint('create_employees', __name__)
update_employees = Blueprint('update_employees', __name__)
del_employees = Blueprint('del_employees', __name__)

# ----------------------------------------------------------------
# CREATE & READ
    # Date: 5/15/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@create_employees.route("/employees", methods=["POST", "GET"])
def employees():
    # --- CREATE / INSERT --- #
    if request.method == "POST":
        # Update data when user clicks "Add Employee"
        if request.form.get("Add_Employee"):
            # User inputs
            theme_park_id = request.form["theme_park_id"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            classification = request.form["classification"]
            email = request.form["email"]
            phone = request.form["phone"]

            # NULL phone value - this is only value allowed to be null.
            if phone == "":
                query = "INSERT INTO employees (first_name, last_name, classification, email, theme_park_id) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (first_name, last_name, classification, email, theme_park_id))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "INSERT INTO employees (first_name, last_name, classification, email, phone, theme_park_id) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (first_name, last_name, classification, email, phone, theme_park_id))
                mysql.connection.commit()

            return redirect("/employees")

    # --- READ /  SELECT --- #
    if request.method == "GET":
        # Query to grab all employee data
        query = """SELECT employee_id, first_name, last_name, classification, email, employees.phone, theme_parks.name from employees
                   INNER JOIN theme_parks ON theme_parks.theme_park_id = employees.theme_park_id;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Theme Park Dropdown
        park_dropdown = "SELECT theme_park_id, name FROM theme_parks;"
        cur = mysql.connection.cursor()
        cur.execute(park_dropdown)
        theme_park_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        print(theme_park_data)
        return render_template("employees.html", data=data, theme_parks=theme_park_data)

# ----------------------------------------------------------------
# DELETE
    # Date: 5/16/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@del_employees.route("/delete_employees/<int:id>")
# --- DELETE --- #
def delete_employees(id):
    query = "DELETE FROM employees WHERE employee_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # Delete page immediately returns us to employees once operation completed
    return redirect("/employees")

# ----------------------------------------------------------------
# UPDATE
    # Date: 5/17/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@update_employees.route("/edit_employees", methods=["POST", "GET"])
def edit_employees():
    if request.method == "POST":
        # Update data when user clicks "Update Employee"
        if request.form.get("Update_Employee"):
            # User inputs
            employee_id = request.form["employee_id"]
            theme_park_id = request.form["theme_park_id"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            classification = request.form["classification"]
            email = request.form["email"]
            phone = request.form["phone"]

            # NULL phone value - this is only value allowed to be null.
            if phone == "":
                query = """UPDATE employees SET employee.first_name = %s, employees.last_name =%s, employees.classification =%s, 
                employees.email = %s, employees.theme_park_id = %s WHERE employees.employee_id %s"""
                cur = mysql.connection.cursor()
                cur.execute(query, (first_name, last_name, classification, email, theme_park_id))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = """UPDATE employees SET employees.first_name = %s, employees.last_name =%s, employees.classification =%s, 
                employees.email = %s, employees.phone =%s, employees.theme_park_id = %s WHERE employees.employee_id =%s"""
                cur = mysql.connection.cursor()
                cur.execute(query, (first_name, last_name, classification, email, phone, theme_park_id, employee_id))
                mysql.connection.commit()

            return redirect('/employees')
