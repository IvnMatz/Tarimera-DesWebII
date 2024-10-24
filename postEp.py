from flask import Blueprint, abort, request, redirect, session, jsonify, url_for
from vFunctions import processor, allowed_file
import pyodbc

rutas_bp = Blueprint('rutas', __name__)
rutas_bp.secret_key = 'butImWithTheHomiesRightNow'
server = '(localdb)\\MainServer'  
database = 'UsersWebP'
UPLOAD_FOLDER = 'static/Uploaded_img/'

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
        cursor.execute(f"INSERT INTO users VALUES({newID}, \'{username}\', \'{password}\', \'{mail}\', 0)")
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('index'))
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

    redir = url_for('search', search_term=pSearchT)

    return redirect(redir)

@rutas_bp.route('/save-product/<id_product>', methods=['POST'])
def saveProduct(id_product):
    userId = session['id']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM saved_product WHERE id_user={userId} AND id_product={id_product}")
        returned = cursor.fetchall()
        if returned:
            cursor.execute(f"DELETE FROM saved_product WHERE id_user={userId} AND id_product={id_product}")
            cursor.commit()
            return jsonify({ 'message' : 'deleted' })

        cursor.execute(f'INSERT INTO saved_product VALUES({userId}, {int(id_product)}) ')
        cursor.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        abort(500)
    
    response = {'message' : 'saved'}
    return jsonify(response)

@rutas_bp.route('/upload_product', methods=['POST'])
def upload_product():
    if 'is_authenticated' not in session:
        return jsonify({'message' : 'problem'})
    if session['id'] != 0:
        return jsonify({'message' : 'problem'})

    if "file" not in request.files:
            return jsonify({'message' : 'problem'})
    
    name = request.form['nombre']
    precio = int(request.form['precio'])
    dim = request.form['dimen']
    weight = int(request.form['peso'])
    desc = request.form['desc']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("select MAX(id_product) from products")
        ret = cursor.fetchall()
        newId = int(ret[0][0]) + 1
        cursor.execute(f"INSERT INTO products VALUES({newId}, \'{name}\', {precio}, \'{desc}\', \'{dim}\', {weight})")
        cursor.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        abort(500)
        
    file = request.files['file']
    if file and allowed_file(file.filename):
        nFilename = f"{newId}.png"
        file.save(f"{UPLOAD_FOLDER}{nFilename}")
        return jsonify({'message' : 'subido'})
    else:
        return jsonify({'message' : 'problem'})

@rutas_bp.route('/c-theme', methods=['POST'])
def c_theme():
    if session['theme'] == 1:
        session['theme'] = 0
    elif session['theme'] == 0:
        session['theme'] = 1

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET theme={session['theme']} where id_user={session['id']}")
        cursor.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        abort(500)
    
    return jsonify({'message' : 'cambiao'})

@rutas_bp.route('/add-cart', methods=['POST'])
def add_cart():
    if 'cart' in session:
        id_product = request.form['id_p']
        quantity = request.form['quantity']
        name = request.form['name']
        price = request.form['price']

        product = [str(id_product), name, price, quantity, int(price) * int(quantity)]
        # 0: ID     1:NOMBRE    2:PRECIO    3:CANTIDAD      4:PRECIO FINAL
        session['cart'].append(product)
        session.modified = True

        return jsonify({'message' : 'agregado'})
    else:
        return jsonify({'message' : 'NoSession'})
    
@rutas_bp.route('/del-cart', methods=['POST'])
def deleteC():
    id_p = request.form['id']

    new_cart = [arr for arr in session['cart'] if arr[0] != str(id_p) ]
    session.pop('cart', None)
    session['cart'] = new_cart
    session.modified = True
    
    return redirect(url_for('cart'))
