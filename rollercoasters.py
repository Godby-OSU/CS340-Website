from flask import  render_template, redirect, request, Blueprint
from app import mysql as mysql

# ----------------------------------------------------------------
# Creating Blueprints
    # Citation for the following methods: Creating Blueprint and labeling routes
    # Date: 5/23/2022
    # Adapted from:
    # Source URL: https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
# ----------------------------------------------------------------
create_rollercoasters = Blueprint('create_rollercoasters', __name__)
update_rollercoasters = Blueprint('update_rollercoasters', __name__)
del_rollercoasters = Blueprint('del_rollercoasters', __name__)

# ----------------------------------------------------------------
# CREATE & READ
    # Date: 5/15/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@create_rollercoasters.route("/rollercoasters", methods=["POST", "GET"])
def rol():
    # --- CREATE / INSERT --- #
    if request.method == "POST":
        # Update data when user clicks "Add Rollercoaster"
        if request.form.get("Add_Rollercoaster"):
            # User inputs
            name = request.form["name"]
            type = request.form["type"]
            length_feet = request.form["length_feet"]
            runtime_seconds = request.form["runtime_seconds"]
            theme_park_id = request.form["theme_park_id"]

            # No NULL inputs
            query = "INSERT INTO rollercoasters (rollercoasters.name, type, length_feet, runtime_seconds, theme_park_id) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type, length_feet, runtime_seconds, theme_park_id))
            mysql.connection.commit()

            return redirect("/rollercoasters")

    # --- READ /  SELECT --- #
    if request.method == "GET":
        # Query to grab all rollercoaster data
        query = """SELECT rollercoaster_id, rollercoasters.name, type, length_feet, rollercoasters.runtime_seconds, theme_parks.name from rollercoasters
                   INNER JOIN theme_parks ON theme_parks.theme_park_id = rollercoasters.theme_park_id;"""
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
        return render_template("rollercoasters.html", data=data, theme_parks=theme_park_data)

# ----------------------------------------------------------------
# DELETE
    # Date: 5/16/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@del_rollercoasters.route("/delete_rollercoasters/<int:id>")
# --- DELETE --- #
def delete_rollercoasters(id):
    query = "DELETE FROM rollercoasters WHERE rollercoaster_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # Delete page immediately returns us to rollercoasters once operation completed
    return redirect("/rollercoasters")

# ----------------------------------------------------------------
# UPDATE
    # Date: 5/17/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@update_rollercoasters.route("/edit_rollercoasters", methods=["POST", "GET"])
def edit_rollercoasters():
    if request.method == "POST":
        # Update data when user clicks "Update Rollercoaster"
        if request.form.get("Update_Rollercoaster"):
            # User inputs
            rollercoaster_id = request.form["rollercoaster_id"]
            name = request.form["name"]
            type = request.form["type"]
            length_feet = request.form["length_feet"]
            runtime_seconds = request.form["runtime_seconds"]
            theme_park_id = request.form["theme_park_id"]

            # No NULL inputs

            query = """UPDATE rollercoasters SET rollercoasters.name =%s, rollercoasters.type =%s, 
            rollercoasters.length_feet = %s, rollercoasters.runtime_seconds =%s, rollercoasters.theme_park_id = %s WHERE rollercoasters.rollercoaster_id =%s"""
            cur = mysql.connection.cursor()
            cur.execute(query, (name, type, length_feet, runtime_seconds, theme_park_id, rollercoaster_id))
            mysql.connection.commit()

            return redirect('/rollercoasters')
