from flask import Blueprint, abort, request, redirect
import pyodbc

rutas_bp = Blueprint('rutas', __name__)
server = '(localdb)\\MainServer'  
database = 'UsersWebP'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

@rutas_bp.route('/register-new-user', methods=['POST'])
def registerN():
    username = request.form['username']  # username, mail, password
    mail = request.form['mail']
    password = request.form['password']
        
    try:
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")
    
        cursor = conn.cursor()

        cursor.execute("SELECT max(id_user) from users")
        MaxID = cursor.fetchall()
        newID = int(MaxID[0][0]) + 1
        cursor.execute(f"INSERT INTO users VALUES({newID}, \'{username}\', \'{password}\', \'{mail}\', \'ES\', 0)")
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("http://localhost:5000")
    except Exception as e:
        abort(500)