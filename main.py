import pyodbc
from flask import Flask, request, render_template

app = Flask(__name__)

# Definir los parámetros de conexión
server = '(localdb)\\MainServer'  
database = 'UsersWebP'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'



# ROUTES ------------------------------------------------------
# Main Route
@app.route("/")
def index():
    return render_template('index.html')

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
            cursor.execute(f"INSERT INTO users VALUES({int(newID)}, \'{str(username)}\', \'{str(password)}\', \'{str(mail)}\')")
            conn.commit()

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al conectar a SQL Server: {e}")

        return 'Registro Completado'
    return render_template('register.html')

# Login Route
@app.route("/Login", methods=['GET', 'POST'])
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
                return 'Sesión Iniciada con Éxito'
            else:
                return 'Usuario o contraseña Mal ingresados'

        except Exception as e:
            print(f"Error al conectar a SQL Server: {e}")

    return render_template('login.html')
