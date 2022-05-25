from flask import render_template, redirect

# ----------------------------------------------------------------
# Import Blueprints
    # Date: 5/23/2022
    # Adapted from:
    # Source URL: https://stackoverflow.com/questions/15231359/split-python-flask-app-into-multiple-files
# ----------------------------------------------------------------
# Import routes
from app import app as app
from app import mysql as mysql

# Employees Page
from employees import create_employees, update_employees, del_employees
app.register_blueprint(create_employees)
app.register_blueprint(update_employees)
app.register_blueprint(del_employees)

# Rollercoasters Page Page
from rollercoasters import create_rollercoasters, update_rollercoasters, del_rollercoasters
app.register_blueprint(create_rollercoasters)
app.register_blueprint(update_rollercoasters)
app.register_blueprint(del_rollercoasters)

# ----------------------------------------------------------------
# Home/Index Routes
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
# Listener - Run website
# ----------------------------------------------------------------
if __name__ == "__main__":
    app.run(port=3000, debug=True)