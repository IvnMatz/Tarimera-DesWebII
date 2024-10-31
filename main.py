import pyodbc
from flask import Flask, request, render_template, session, redirect, url_for, abort
from handleErrors import error_handlers_bp
from postEp import rutas_bp
from vFunctions import processor, loader

UPLOAD_FOLDER = 'static/Uploaded_img'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(error_handlers_bp)
app.register_blueprint(rutas_bp)
app.secret_key = 'butImWithTheHomiesRightNow'

# Parametros Conexión SQL Server
server = '(localdb)\\MainServer'  
database = 'UsersWebP'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# ROUTES ----------------------------------------------------------------------------
# Main Route--------------------------------------------------------------------------
@app.route("/")
def index():
    try:
        top = loader('topP.json')
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")
        cursor = conn.cursor()
        cursor.execute(f"select id_product, nombre, price from products where id_product={top[0]}")
        Prod = cursor.fetchall()
        returnedProd = []
        returnedProd.append(Prod[0])
        cursor.execute(f"select id_product, nombre, price from products where id_product={top[1]}")
        Prod = cursor.fetchall()
        returnedProd.append(Prod[0])
        cursor.execute(f"select id_product, nombre, price from products where id_product={top[2]}")
        prod = cursor.fetchall()
        returnedProd.append(prod[0])
        cursor.close()
        conn.close()
        
    except Exception as e:
        return render_template("error.html", error=e, code=f"img/500.png")

    if 'is_authenticated' in session:
        return render_template('index.html', user=session, theme=session['theme'], products=returnedProd)
    else:
        return render_template('index.html', user=False, theme=0, products=returnedProd)
    

# Register Route --------------------------------------------------------------------
@app.route("/register", methods=['GET'])
def register():
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
                session['pwrd'] = returnedUser[0][2]
                session['mail'] = returnedUser[0][3]
                session['theme'] = returnedUser[0][4]
                session['cart'] = []
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))

        except Exception as e:
            return render_template("error.html", error=e, code=f"img/500.png")

    return render_template('login.html')

#User Route -------------------------------------------------------------------------------
@app.route('/user')
def userpage():
    user = session

    if 'id' not in session:
        abort(403)

    rQuery = f""" select products.nombre, review.title, review.calif, review.descript from review
     join products on review.id_product=products.id_product 
join users on review.id_user = users.id_user where review.id_user={session['id']}
 """
    sQuery = f""" select products.nombre, products.price, products.id_product from saved_product
join products on saved_product.id_product=products.id_product
where saved_product.id_user={session['id']} """
    try:
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")

        cursor = conn.cursor()

        cursor.execute(rQuery)
        reviews = cursor.fetchall()
        cursor.execute(sQuery)
        savedProd = cursor.fetchall()

        cursor.close()
        conn.close()
    except Exception as e:
            return render_template("error.html", error=e, code=f"img/500.png")
    
    if 'is_authenticated' in session:
        return render_template("user.html", user=user, savedProd=savedProd, reviews=reviews, theme=session['theme'])

#Product Route ---------------------------------------------------------------------------------
@app.route('/product/<id_product>')
def product(id_product):
    product = {}
    calif = {}

    post_a = "/post-a-review/" + str(id_product)
    save = '/save-product/' + str(id_product)
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

        if returnedRev:
            cursor.execute(f"SELECT sum(calif), count(id_review) from review where id_product = {id_product}")
            starsC = cursor.fetchall()
            calif['sum'] = starsC[0][1]
            calif['avg'] = round(starsC[0][0] / starsC[0][1], 2)
            cursor.execute(f" SELECT count(id_review) from review where id_product={id_product} AND calif=5")
            rol = cursor.fetchall()
            calif['Fstarsper'] = round(( rol[0][0] / starsC[0][1] ) * 100)
            cursor.execute(f" SELECT count(id_review) from review where id_product={id_product} AND calif=4")
            rol = cursor.fetchall()
            calif['Fostarsper'] = round(( rol[0][0] / starsC[0][1] ) * 100)
            cursor.execute(f" SELECT count(id_review) from review where id_product={id_product} AND calif=3")
            rol = cursor.fetchall()
            calif['Tstarsper'] = round(( rol[0][0] / starsC[0][1] ) * 100)
            cursor.execute(f" SELECT count(id_review) from review where id_product={id_product} AND calif=2")
            rol = cursor.fetchall()
            calif['Tostarsper'] = round(( rol[0][0] / starsC[0][1] ) * 100)
            cursor.execute(f" SELECT count(id_review) from review where id_product={id_product} AND calif=1")
            rol = cursor.fetchall()
            calif['Ostarsper'] = round(( rol[0][0] / starsC[0][1] ) * 100)
        else:
            calif = False

        cursor.close()
        conn.close()
        
        if returnedProd:
            product['id'] = returnedProd[0][0]
            product['name'] = returnedProd[0][1]
            product['precio'] = returnedProd[0][2]
            product['desc'] = returnedProd[0][3]
            product['dimension'] = returnedProd[0][4]
            product['peso'] = returnedProd[0][5]
        else:
            abort(404)

    except Exception as e:
        return render_template("error.html", error=e, code=f"img/500.png")
    
    if 'is_authenticated' in session:
        return render_template("product.html", product=product, reviews=returnedRev, user=session, post=post_a, save=save, theme=session['theme'], calif=calif)
    else:
        return render_template("product.html", product=product, reviews=returnedRev, user=False, theme=0, calif=calif)
    

# ADMIN PAGE ROUTE -----------------------------------------------------------------------------
@app.route('/admin', methods=['GET'])
def admin():  
    if 'is_authenticated' not in session:
        abort(403)
    else:
        print(session)
        if session['id'] == 0:
            try:
                top = loader('topP.json')
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute("select id_product, nombre from products")
                products = cursor.fetchall()
                cursor.close()
                conn.close()
            except:
                abort(500)
            return render_template("admin.html", user=session, theme=session['theme'], products = products, top=top)
        else:
            abort(403)

# SEARCH ROUTE ----------------------------------------------------------------------------------
@app.route('/search/<search_term>', methods=['GET'])
def search(search_term):
    pSearchT = processor(search_term)

    try:
        conn = pyodbc.connect(conn_str)
        print("Conexión exitosa")
        cursor = conn.cursor()
        cursor.execute(f"select id_product, nombre, price from products where nombre like \'%{pSearchT}%\'")
        returnedP = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        return render_template("error.html", error=e, code=f"img/404.png")
    
    if 'is_authenticated' in session:
        return render_template('searched.html', SearchTerm=pSearchT, products=returnedP, user=session, theme=session['theme'])
    else:
        return render_template("searched.html", SearchTerm=pSearchT, products=returnedP, user=False, theme=0)
    

#cart route -------------------------------------------------------------------------------------
@app.route('/cart')
def cart():
    if 'cart' not in session:
        return redirect(url_for('index'))
    leng = len(session['cart'])
    print(session['cart'])
    return render_template('cart.html', is_prod=leng, cart=session['cart'], user=session, theme=session['theme'] )

#UPDATE USER ROUTE ------------------------------------------------------------------------------
@app.route('/update-user')
def updateU():
    return render_template('editProf.html', name=session['username'], mail=session['mail'], passw=session['pwrd'])


#logout route (Redirects to index) --------------------------------------------------------------
@app.route('/logout')
def logout():
    session.pop('is_authenticated', None)
    session.pop('username', None)
    session.pop('pwrd', None)
    session.pop('id', None)
    session.pop('mail', None)
    session.pop('theme', None)
    session.pop('cart', None)
    return redirect(url_for('index'))

## CORRER EL PROGRAMA ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(threaded=True)