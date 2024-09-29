import pyodbc
from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'butImWithTheHomiesRightNow'

# Definir los parámetros de conexión
server = '(localdb)\\MainServer'  
database = 'UsersWebP'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'



# ROUTES ----------------------------------------------------------------------------
# Main Route--------------------------------------------------------------------------
@app.route("/")
def index():
    user = {}
    if 'username' in session:
        user['auth'] = session['is_authenticated']
    else:
        user['auth'] = False
    return render_template('index.html', user=user)

#ERROR HANDLER FUNCTIONS--------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", error=f"{e.code} {e.description}"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", error=f"{e.code} {e.description}"), 500

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
            return render_template("error.html", error=e)

        
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
                session['lang'] = returnedUser[0][4]
                session['theme'] = returnedUser[0][5]
                return redirect(url_for('index'))
            else:
                return 'Usuario o contraseña Mal ingresados'

        except Exception as e:
            return render_template("error.html", error=e)

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
            return render_template("error.html", error="Página no encontrada")

    except Exception as e:
        return render_template("error.html", error=e)
    
    return render_template("product.html", product=product, reviews=returnedRev)

#logout route (Redirects to index) --------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('is_athenticated', None)
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('index'))
