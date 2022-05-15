from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# ----------------------------------------------------------------
# Configure Data Base
# ----------------------------------------------------------------

app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_godbyg"
app.config["MYSQL_PASSWORD"] = "XXXX"
app.config["MYSQL_DB"] = "cs340_godbyg"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# ----------------------------------------------------------------
# Home/Index Routes
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
# Employees Page
# ----------------------------------------------------------------


@app.route("/employees", methods=["POST", "GET"])
def employees():
    # --- CREATE / INSERT --- #
    if request.method == "POST":
        # Activated by Add Employee Button
        if request.form.get("Add_Person"):
            # User inputs
            theme_park_id = request.form["theme_park_id"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            classification = request.form["classification"]
            email = request.form["email"]
            phone = request.form["phone"]

            # NULL phone value - this is only value allowed to be null.
            if phone == "":
                query = "INSERT INTO employees (theme_park_id, first_name, last_name, classification, email) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (theme_park_id, first_name, last_name, classification, email))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = "INSERT INTO employees (theme_park_id, first_name, last_name, classification, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (theme_park_id, first_name, last_name, classification, email, phone))
                mysql.connection.commit()

            # Redirect to Employees
            return redirect("/employees")

    # --- READ /  SELECT --- #
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = """SELECT first_name, last_name, classification, email, employees.phone, theme_parks.name from employees
                   INNER JOIN theme_parks ON theme_parks.theme_park_id = employees.theme_park_id;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Theme Park Dropdown
        park_dropdown = "SELECT theme_park_id, name FROM theme_parks;"   # named query 2 in example
        cur = mysql.connection.cursor()
        cur.execute(park_dropdown)
        park_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("employees.html", data=data, theme_parks=park_data)

# -------------------------------------------------------------------------------------------------- #

# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_people/<int:id>")
def delete_people(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM bsg_people WHERE id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/people")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_people/<int:id>", methods=["POST", "GET"])
def edit_people(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM bsg_people WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_people.j2", data=data, homeworlds=homeworld_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Person"):
            # grab user form inputs
            id = request.form["personID"]
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]

            # account for null age AND homeworld
            if (age == "" or age == "None") and homeworld == "0":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == "0":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age, id))
                mysql.connection.commit()

            # account for null age
            elif age == "" or age == "None":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/people")

# ----------------------------------------------------------------
# Listener - run website
# ----------------------------------------------------------------

if __name__ == "__main__":
    app.run(port=3000, debug=True)