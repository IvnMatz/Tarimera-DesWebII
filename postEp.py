from flask import Blueprint, abort, request, redirect, session, jsonify
from vFunctions import processor
import pyodbc

rutas_bp = Blueprint('rutas', __name__)
server = '(localdb)\\MainServer'  
database = 'UsersWebP'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# RUTAS ---------------------------------------------------------------------

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

@rutas_bp.route('/post-a-review/<id_product>', methods=['POST'])
def postReview(id_product):
    userId = session['id']
    title = request.form['title']
    calif = request.form['range']
    desc = request.form['description']

    if title == "" or desc == "":
        response = { 'message' : 'Vacia' }
        return jsonify(response)

    calif = int(calif)

    try:
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")
        cursor = conn.cursor()

        cursor.execute("select max(id_review) from review")
        maxId = cursor.fetchall()
        if maxId == 0:
            newID = 0
        else:
            newID = int(maxId[0][0]) + 1
            
            cursor.execute(f"INSERT into review VALUES({newID}, \'{title}\', \'{desc}\', {calif}, {userId}, {int(id_product)} )")
            cursor.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        abort(500)

    response = { 'message' : 'ok' }
    return jsonify(response)

@rutas_bp.route('/search-p', methods=['POST'])
def searchP():
    searchT = request.form['search']
    pSearchT = processor(searchT)

    redir = "http://localhost:5000/" "search/" + pSearchT

    return redirect(redir)
