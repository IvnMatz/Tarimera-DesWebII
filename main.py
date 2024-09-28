import pyodbc
from flask import Flask, request, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'papuClave'

# Definir los parámetros de conexión
server = '(localdb)\\MainServer'  
database = 'UsersWebP'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'



# ROUTES ------------------------------------------------------
# Main Route
@app.route("/")
def index():
    user = {}
    if 'username' in session:
        user['auth'] = session['is_authenticated']
    else:
        user['auth'] = False
    return render_template('index.html', user=user)

# Register Route
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
            return f"Error {e}"

        
    return render_template('register.html')

# Login Route
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
                session['username'] = username
                session['id'] = returnedUser[0][0]
                session['is_authenticated'] = True
                return 'Sesión iniciada !'
            else:
                return 'Usuario o contraseña Mal ingresados'

        except Exception as e:
            return f"Error {e}"

    return render_template('login.html')

@app.route('/user')
def userpage():
    return render_template("profPage.html")

@app.route('/product/<id_product>')
def product(id_product):
    return f"Producto {id_product}"

@app.route('/logout')
def logout():
    session.pop('is_athenticated', None)
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('login'))
