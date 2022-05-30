from flask import  render_template, redirect, request, Blueprint
from app import mysql as mysql

# ----------------------------------------------------------------
# Creating Blueprints
    # Citation for the following methods: Creating Blueprint and labeling routes
    # Date: 5/23/2022
    # Adapted from:
    # Source URL: https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
# ----------------------------------------------------------------
create_certificate = Blueprint('create_certificate', __name__)
update_certificate = Blueprint('update_certificate', __name__)
del_certificate = Blueprint('del_certificate', __name__)

# ----------------------------------------------------------------
# CREATE & READ
    # Date: 5/15/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@create_certificate.route("/certificate", methods=["POST", "GET"])
def certificate():
    # --- CREATE / INSERT --- #
    if request.method == "POST":
        # Update data when user clicks "Add Employee"
        if request.form.get("Add_Certificate"):
            # User inputs
            cert_id             = request.form["cert_id"]            
            cert_type           = request.form["type"]
            cert_agency         = request.form["agency"]
            cert_pay_increase   = request.form["pay_increase"]           

            # NULL cert_agency and cert_pay_increase
            if cert_agency == "" and cert_pay_increase == "":
                query = """
                INSERT INTO certifications 
                    (cert_id, cert_type) 
                VALUES 
                    (%s, %s)
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (cert_id, cert_type))
                mysql.connection.commit()

            # NULL cert_agency
            elif cert_agency == "":
                query = """
                INSERT INTO certifications 
                    (cert_id, cert_type, cert_pay_increase) 
                VALUES 
                    (%s, %s, %s)
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (cert_id, cert_type, cert_pay_increase))
                mysql.connection.commit()

            # NULL cert_pay_increase
            elif cert_pay_increase == "":
                query = """
                INSERT INTO certifications 
                    (cert_id, cert_type, cert_agency) 
                VALUES 
                    (%s, %s, %s)
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (cert_id, cert_type, cert_agency))
                mysql.connection.commit()


            # No NULL inputs
            else:
                query = """
                INSERT INTO certifications 
                (cert_id, cert_type, cert_agency, cert_pay_increase) 
                VALUES (%s, %s, %s, %s)
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
                mysql.connection.commit()

            return redirect("/certificates")

    # --- READ /  SELECT --- #
    if request.method == "GET":
        # Query to grab all employee data
        query = """
        SELECT 
            cert_id, type, agency, pay_increase 
        FROM 
            certifications;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Certficiation Dropdown
        park_dropdown = """
        SELECT 
            cert_id, agency 
        FROM 
            certifications;
        """
        cur = mysql.connection.cursor()
        cur.execute(park_dropdown)
        certificates_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        print(certificates_data)
        return render_template("certificates.html", data=data, certificates=certificates_data)





# ----------------------------------------------------------------
# DELETE
    # Date: 5/16/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@del_certificate.route("/delete_certificates/<int:id>")
# --- DELETE --- #
def delete_certificate(id):
    query = """
    DELETE FROM 
        certifications 
    WHERE 
        cert_id = '%s';
    """
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # Delete page immediately returns us to certificates once operation completed
    return redirect("/certificates")






# ----------------------------------------------------------------
# UPDATE
    # Date: 5/17/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@update_certificate.route("/edit_certificate", methods=["POST", "GET"])
def edit_certificate():
    if request.method == "POST":
        # Update data when user clicks "Update Employee"
        if request.form.get("Update_Certificates"):
            # User inputs
            cert_id             = request.form["cert_id"]            
            cert_type           = request.form["type"]
            cert_agency         = request.form["agency"]
            cert_pay_increase   = request.form["pay_increase"]                        

            # NULL cert_agency value and cert_pay_increase.
            if cert_agency == "" and cert_pay_increase == "":
                query = """
                UPDATE 
                    certifications
                SET 
                    cert_id              = %s,
                    cert_type            = %s,
                    cert_agency          = NULL, 
                    cert_pay_increase    = NULL,                     
                WHERE
                    cert_id              = %s
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
                mysql.connection.commit()

            # NULL cert_agency
            elif cert_agency == "":
                query = """
                UPDATE 
                    certifications
                SET 
                    cert_id              = %s,
                    cert_type            = %s,
                    cert_agency          = NULL, 
                    cert_pay_increase    = %s,                     
                WHERE
                    cert_id              = %s
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
                mysql.connection.commit()

            # NULL cert_pay_increase
            elif cert_pay_increase == "":
                query = """
                UPDATE 
                                    SET 
                    cert_id              = %s,
                    cert_type            = %s,
                    cert_agency          = %s, 
                    cert_pay_increase    = NULL,                     
                WHERE
                    cert_id              = %s
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
                mysql.connection.commit()

            # No NULL inputs
            else:
                query = """
                UPDATE 
                    certifications
                SET 
                    cert_id              = %s,
                    cert_type            = %s,
                    cert_agency          = %s, 
                    cert_pay_increase    = %s,                     
                WHERE
                    cert_id              = %s
                """
                cur = mysql.connection.cursor()
                cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
                mysql.connection.commit()

            return redirect('/certificates')
