from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# ----------------------------------------------------------------
# Configure Data Base
    # Citation for the following configuration:
    # Date: 5/15/2022
    # Copied from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_x"
app.config["MYSQL_PASSWORD"] = "xxxx"
app.config["MYSQL_DB"] = "cs340_x"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# ----------------------------------------------------------------
# Home/Index Routes
    # Citation for the following methods:
    # Date: 5/15/2022
    # Copied from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
# Home Page Redirect
@app.route("/")
def home():
    return redirect("/index")

# Index Route
@app.route("/index")
def index():
    return render_template('index.html')

# ----------------------------------------------------------------
# CREATE & READ
    # Citation for the following methods:
    # Date: 5/15/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@app.route("/employees", methods=["POST", "GET"])
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
    # Citation for the following methods:
    # Date: 5/16/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@app.route("/delete_employees/<int:id>")
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
    # Citation for the following methods:
    # Date: 5/17/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@app.route("/edit_employees", methods=["POST", "GET"])
def edit_people():
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

# ----------------------------------------------------------------
# Listener - Run website
# ----------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=18214, debug=True)