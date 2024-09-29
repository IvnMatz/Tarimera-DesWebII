import pyodbc
from flask import Flask, request, render_template, session, redirect, url_for, abort
from handleErrors import error_handlers_bp
import os

UPLOAD_FOLDER = 'static/Uploaded_img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(error_handlers_bp)
app.secret_key = 'butImWithTheHomiesRightNow'

# Definir los parámetros de conexión
server = '(localdb)\\MainServer'  
database = 'UsersWebP'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ROUTES ----------------------------------------------------------------------------
# Main Route--------------------------------------------------------------------------
@app.route("/")
def index():
    if 'is_authenticated' in session:
        return render_template('index.html', user=session['is_authenticated'], theme=session['theme'])
    else:
        return render_template('index.html', user=False, theme=0)
    

# Register Route --------------------------------------------------------------------
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']  # username, mail, password
        mail = request.form['mail']
        password = request.form['password']
        
        try:
            conn = pyodbc.connect(conn_str)
            print("Conexión exitosa")
    
            cursor = conn.cursor()

            cursor.execute("SELECT max(id_user) from users")
            MaxID = cursor.fetchall()
            for row in MaxID:
                newID = int(row[0]) + 1
            cursor.execute(f"INSERT INTO users VALUES({newID}, \'{username}\', \'{password}\', \'{mail}\', \'ES\', 0)")
            conn.commit()

            cursor.close()
            conn.close()

            return "registro completo"
        except Exception as e:
            return render_template("error.html", error=e, code=f"img/500.png")

        
    return render_template('register.html')

# Login Route -------------------------------------------------------------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']  # username, password
        password = request.form['password']
        
        try:
            conn = pyodbc.connect(conn_str)
            print("Conexión exitosa")
    
            cursor = conn.cursor()

            cursor.execute(f"select * from users where username=\'{username}\' and passw=\'{password}\'")
            returnedUser = cursor.fetchall()

            cursor.close()
            conn.close()
            if returnedUser:
                session['username'] = returnedUser[0][1]
                session['id'] = returnedUser[0][0] # 0=ID 1=Username 2=Password 3=Mail 4=Language 5=theme (0=light, 1=Dark)
                session['is_authenticated'] = True
                session['mail'] = returnedUser[0][3]
                #session['lang'] = returnedUser[0][4]
                session['theme'] = returnedUser[0][5]
                return redirect(url_for('index'))
            else:
                return 'Usuario o contraseña Mal ingresados'

        except Exception as e:
            return render_template("error.html", error=e, code=f"img/500.png")

    return render_template('login.html')

#User Route -------------------------------------------------------------------------------
@app.route('/user')
def userpage():
    user = session
    return render_template("user.html", user=user)

#Product Route ---------------------------------------------------------------------------------
@app.route('/product/<id_product>')
def product(id_product):
    product = {}
    try:
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")
        cursor = conn.cursor()
        cursor.execute(f"select * from products where id_product={id_product}")
        returnedProd = cursor.fetchall()
        #ID del array (returnedprod[0][ESTO])
        # 0=ID 1=name 2=precio 3=descript 4=dimension 5=peso
        cursor.execute(f"select users.username, review.* from review join users on review.id_user=users.id_user join products on review.id_product=products.id_product where products.id_product={id_product}")
        returnedRev = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if returnedProd:
            product['name'] = returnedProd[0][1]
            product['precio'] = returnedProd[0][2]
            product['desc'] = returnedProd[0][3]
            product['dimension'] = returnedProd[0][4]
            product['peso'] = returnedProd[0][5]
        else:
            abort(404)

    except Exception as e:
        return render_template("error.html", error=e, code=f"img/500.png")
    
    return render_template("product.html", product=product, reviews=returnedRev)

# ADMIN PAGE ROUTE -----------------------------------------------------------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if "file" not in request.files:
            return "No se encontró ningún archivo"
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Archivo subido"
        else:
            return "Archivo no aceptado"
    if 'is_authenticated' not in session:
        abort(403)
    else:
        print(session)
        if session['id'] == 0:
            return render_template("admin.html")
        else:
            abort(403)

#logout route (Redirects to index) --------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('is_authenticated', None)
    session.pop('username', None)
    session.pop('id', None)
    session.pop('mail', None)
    session.pop('lang', None)
    session.pop('theme', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()