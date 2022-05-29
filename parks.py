from flask import  render_template, redirect, request, Blueprint
from app import mysql as mysql

# ----------------------------------------------------------------
# Creating Blueprints
    # Citation for the following methods: Creating Blueprint and labeling routes
    # Date: 5/23/2022
    # Adapted from:
    # Source URL: https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
# ----------------------------------------------------------------
create_theme_park = Blueprint('cr_theme_park', __name__)
update_theme_park = Blueprint('u_theme_park', __name__)
del_theme_park = Blueprint('d_theme_park', __name__)

# ----------------------------------------------------------------
# CREATE & READ
    # Date: 5/15/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@create_theme_park.route("/parks", methods=["POST", "GET"])
def theme_park():
    # --- CREATE / INSERT --- #
    if request.method == "POST":
        # Update data when user clicks "Add Employee"
        if request.form.get("Add_Theme_park"):
            # User inputs
            # theme_park_id = request.form["theme_park_id"]
            name            = request.form["name"]
            capacity        = request.form["capacity"]
            admission_fee   = request.form["admission_fee"]
            phone           = request.form["phone"]

            # NULL phone value - this is only value allowed to be null.
            if phone == "":
                query = "INSERT INTO employees (name, capacity, admission_fee, phone) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, capacity, admission_fee, phone))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "INSERT INTO employees (name, capacity, admission_fee, phone) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (name, capacity, admission_fee, phone))
                mysql.connection.commit()

            return redirect("/parks")


    # --- READ /  SELECT --- #
    if request.method == "GET":
        # Query to grab all employee data
        query = """SELECT theme_park_id, name, capacity, admission_fee, phone FROM theme_parks"""
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
        return render_template("parks.html", data=data, theme_parks=theme_park_data)

# ----------------------------------------------------------------
# DELETE
    # Date: 5/16/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@del_theme_park.route("/delete_theme_park/<int:id>")
# --- DELETE --- #
def delete_theme_park(id):
    query = "DELETE FROM theme_parks WHERE theme_park_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # Delete page immediately returns us to employees once operation completed
    return redirect("/parks")

# ----------------------------------------------------------------
# UPDATE
    # Date: 5/17/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@update_theme_park.route("/edit_theme_park", methods=["POST", "GET"])
def edit_people():
    if request.method == "POST":
        # Update data when user clicks "Update Employee"
        if request.form.get("Update_Theme_park"):
            # User inputs
            theme_park_id   = request.form["theme_park_id"]
            name            = request.form["name"]
            capacity        = request.form["capacity"]
            admission_fee   = request.form["admission_fee"]
            phone           = request.form["phone"]

            # NULL phone value - this is only value allowed to be null.
            if phone == "":
                query = """
                UPDATE theme_parks 
                SET name = %s, capacity = %s, admission_fee = %s, phone = %s,                 
                WHERE theme_parks_id = %s
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (name, capacity, admission_fee, phone, theme_park_id))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = """
                UPDATE theme_parks  
                SET name = %s, capacity = %s, admission_fee = %s, phone = %s,                 
                WHERE theme_parks_id = %s
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (name, capacity, admission_fee, phone, theme_park_id))
                mysql.connection.commit()

            return redirect('/parks')
