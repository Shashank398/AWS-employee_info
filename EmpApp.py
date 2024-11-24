from flask import Flask, render_template, request
from pymysql import connections
import os
from config import *

app = Flask(__name__)

# AWS RDS Configuration
db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')

@app.route("/addemp", methods=['POST'])
def AddEmp():
    name = request.form['name']
    email = request.form['email']

    insert_sql = "INSERT INTO employee (name, email) VALUES (%s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (name, email))
        db_conn.commit()
        emp_name = name
    except Exception as e:
        db_conn.rollback()
        return f"Error occurred: {e}"
    finally:
        cursor.close()

    return render_template('AddEmpOutput.html', name=emp_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
