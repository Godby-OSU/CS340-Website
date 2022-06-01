from flask import  render_template, redirect, request, Blueprint
from app import mysql as mysql

# ----------------------------------------------------------------
# Creating Blueprints
    # Citation for the following methods: Creating Blueprint and labeling routes
    # Date: 5/23/2022
    # Adapted from:
    # Source URL: https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
# ----------------------------------------------------------------
create_certificates = Blueprint('create_certificates', __name__)
update_certificates = Blueprint('update_certificates', __name__)
del_certificates = Blueprint('del_certificates', __name__)

# ----------------------------------------------------------------
# CREATE & READ
    # Date: 5/15/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@create_certificates.route("/certificates", methods=["POST", "GET"])
def certificates():    
    # --- CREATE / INSERT --- #
    if request.method == "POST":                
        # Update data when user clicks "Add Employee"
        if request.form.get("Add_Certificates"):

            print('3: certificates')

            # User inputs
            #cert_id             = request.form["cert_id"]            
            cert_type           = request.form["type"]
            cert_agency         = request.form["agency"]
            cert_pay_increase   = request.form["pay_increase"]           



            # # NULL cert_agency and cert_pay_increase
            # if cert_agency == "" and cert_pay_increase == "":
            #     query = """
            #     INSERT INTO certifications 
            #         (cert_id, cert_type) 
            #     VALUES 
            #         (%s, %s)
            #     """
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (cert_id, cert_type))
            #     mysql.connection.commit()

            # # NULL cert_agency
            # elif cert_agency == "":
            #     query = """
            #     INSERT INTO certifications 
            #         (cert_id, cert_type, cert_pay_increase) 
            #     VALUES 
            #         (%s, %s, %s)
            #     """
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (cert_id, cert_type, cert_pay_increase))
            #     mysql.connection.commit()

            # # NULL cert_pay_increase
            # elif cert_pay_increase == "":
            #     query = """
            #     INSERT INTO certifications 
            #         (cert_id, cert_type, cert_agency) 
            #     VALUES 
            #         (%s, %s, %s)
            #     """
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (cert_id, cert_type, cert_agency))
            #     mysql.connection.commit()

            # # No NULL inputs
            # else:
            query = """INSERT INTO certifications (type, agency, pay_increase) VALUES (%s, %s, %s);"""
            cur = mysql.connection.cursor()
            cur.execute(query, (cert_type, cert_agency, cert_pay_increase))
            mysql.connection.commit()
            return redirect("/certificates")



    # --- READ /  SELECT --- #
    if request.method == "GET":
        # Query to grab all certificate data and displays on the subject page
        query = """
        SELECT 
            cert_id, type, agency, pay_increase 
        FROM 
            certifications;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Certficiation Dropdown for update
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
        # print(certificates_data)
        return render_template("certificates.html", data=data, certificates=certificates_data)





# ----------------------------------------------------------------
# DELETE
    # Date: 5/16/2022
    # Adapted from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
@del_certificates.route("/delete_certificates/<int:id>")
# --- DELETE --- #
def delete_certificates(id):
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
@update_certificates.route("/edit_certificates", methods=["POST", "GET"])
def edit_certificates():

    print("1: update cert")
    if request.method == "POST":
        print("2: update cert")
        # Update data when user clicks "Update Employee"
        if request.form.get("Update_Certificates"):
           
            print("3: update cert")
            # User inputs
            cert_id             = request.form["cert_id"]            
            cert_type           = request.form["type"]
            cert_agency         = request.form["agency"]
            cert_pay_increase   = request.form["pay_increase"]                        

            
            print("cert_id", cert_id)
            print("cert_type", cert_type)
            print("cert_agency", cert_agency)
            print("cert_pay_increase", cert_pay_increase)
            # NULL cert_agency value and cert_pay_increase.
            # if cert_agency == "" and cert_pay_increase == "":
            #     query = """
            #     UPDATE 
            #         certifications
            #     SET 
            #         cert_id            = %s,
            #         type               = %s,
            #         agency             = NULL, 
            #         pay_increase       = NULL,                     
            #     WHERE
            #         cert_id              = %s
            #     """
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
            #     mysql.connection.commit()

            # # NULL cert_agency
            # elif cert_agency == "":
            #     query = """
            #     UPDATE 
            #         certifications
            #     SET 
            #             cert_id         = %s,
            #             type            = %s,
            #             agency          = NULL, 
            #             pay_increase    = %s,                     
            #     WHERE
            #         cert_id              = %s
            #     """
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
            #     mysql.connection.commit()

            # # NULL cert_pay_increase
            # elif cert_pay_increase == "":
            #     query = """
            #     UPDATE 
            #         SET 
            #         cert_id         = %s,
            #         type            = %s,
            #         agency          = %s, 
            #         pay_increase    = NULL,                     
            #     WHERE
            #         cert_id              = %s
            #     """
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
            #     mysql.connection.commit()

            # # No NULL inputs
            # else:
            #     query = """
            #     UPDATE 
            #         certifications
            #     SET 
            #         cert_id         = %s,
            #         type            = %s,
            #         agency          = %s, 
            #         pay_increase    = %s,                     
            #     WHERE
            #         cert_id          = %s
            #     """
            #     cur = mysql.connection.cursor()
            #     cur.execute(query, (cert_id, cert_type, cert_agency, cert_pay_increase))
            #     mysql.connection.commit()


            print("4: update cert")
            query = """
            UPDATE 
                certifications
            SET 
                type            = %s,
                agency          = %s, 
                pay_increase    = %s                     
            WHERE
                cert_id         = %s;
            """

            print("\n\n***Query:", query)

            cur = mysql.connection.cursor()
            #print("\n\n***Query excute: ", cur.execute(query, (cert_type, cert_agency, cert_pay_increase)))
            cur.execute(query, (cert_type, cert_agency, cert_pay_increase, cert_id))
            mysql.connection.commit()


            print("5: update cert") 
            return redirect('/certificates')
