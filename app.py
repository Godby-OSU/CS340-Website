from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# ----------------------------------------------------------------
# Configure Database
    # Citation for the following configuration:
    # Date: 5/15/2022
    # Copied from:
    # Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
# ----------------------------------------------------------------
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_lovest"
app.config["MYSQL_PASSWORD"] = "6564"
app.config["MYSQL_DB"] = "cs340_lovest"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)