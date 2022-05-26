from flask import  render_template, redirect, request, Blueprint
from app import mysql as mysql

# ----------------------------------------------------------------
# Creating Blueprints
    # Citation for the following methods: Creating Blueprint and labeling routes
    # Date: 5/23/2022
    # Adapted from:
    # Source URL: https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
# ----------------------------------------------------------------
create_issued_cert = Blueprint('create_issued_cert', __name__)
update_issued_cert = Blueprint('update_issued_cert', __name__)
del_issued_cert = Blueprint('del_issued_cert', __name__)

# ----------------------------------------------------------------
# CREATE & READ
    # Date: 5/15/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@create_issued_cert.route("/issued-certifications", methods=["POST", "GET"])
def issued_cert():
    # --- CREATE / INSERT --- #
    if request.method == "POST":
        # Update data when user clicks "Add Employee"
        if request.form.get("add_issued_cert"):
            # User inputs
            cert_id = request.form["cert_id"]
            employee_id = request.form["employee_id"]
            cert_earned_date = request.form["cert_earned_date"]
            cert_expiration_date = request.form["cert_expiration_date"]

            # No NULL inputs
            query = "INSERT INTO issued_certifications (cert_id, employee_id, cert_earned_date, cert_expiration_date) VALUES (%s, %s, %s, %s)"
            print(query)
            cur = mysql.connection.cursor()
            cur.execute(query, (cert_id, employee_id, cert_earned_date, cert_expiration_date))
            mysql.connection.commit()

            return redirect("/issued-certifications")

    # --- READ /  SELECT --- #
    if request.method == "GET":
        # Query to grab all employee data
        query = """SELECT issued_cert_id, certifications.type, employees.first_name, employees.last_name, cert_earned_date, cert_expiration_date from issued_certifications
                INNER JOIN employees ON employees.employee_id = issued_certifications.employee_id
                INNER JOIN certifications ON certifications.cert_id = issued_certifications.cert_id;"""
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Employee Dropdown
        employee_data = "SELECT employee_id, employees.first_name FROM employees;"
        cur = mysql.connection.cursor()
        cur.execute(employee_data)
        employee_data = cur.fetchall()

        # Cert Dropdown
        cert_data = "SELECT cert_id, type FROM certifications;"
        cur = mysql.connection.cursor()
        cur.execute(cert_data)
        cert_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("issued-certifications.html", data=data, employee_data=employee_data, cert_data=cert_data)

# ----------------------------------------------------------------
# DELETE
    # Date: 5/16/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@del_issued_cert.route("/delete_issued_cert/<int:issued_cert_id>")
# --- DELETE --- #
def delete_issued_cert(issued_cert_id):
    query = "DELETE FROM issued_certifications WHERE issued_cert_id = '%s'"
    
    cur = mysql.connection.cursor()
    cur.execute(query, (issued_cert_id,))
    mysql.connection.commit()

    # Delete page immediately returns us to issued_cert once operation completed
    return redirect("/issued-certifications")

# ----------------------------------------------------------------
# UPDATE
    # Date: 5/17/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@update_issued_cert.route("/edit_issued_cert", methods=["POST", "GET"])
def edit_issued_cert():
    if request.method == "POST":
        # Update data when user clicks "Update Employee"
        if request.form.get("edit_issued_cert"):
            # User inputs
            issued_cert_id = request.form["issued_cert_id"]
            cert_id = request.form["cert_id"]
            employee_id = request.form["employee_id"]
            cert_earned_date = request.form["cert_earned_date"]
            cert_expiration_date = request.form["cert_expiration_date"]


            query = """UPDATE issued_certifications SET cert_id = %s, employee_id =%s, cert_earned_date =%s, 
            cert_expiration_date = %s WHERE issued_cert_id = %s"""
            print("DOING IT")
            print(issued_cert_id, cert_id, employee_id, cert_earned_date, cert_expiration_date)
            cur = mysql.connection.cursor()
            cur.execute(query, (issued_cert_id, cert_id, employee_id, cert_earned_date, cert_expiration_date))
            mysql.connection.commit()

            return redirect('/issued-certifications')
