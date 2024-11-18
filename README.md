# Intento de documentación
### Instalación
1. Por obviedad, Python instalado.
2. un venv dentro de la carpeta, así que ```python -m venv venv```
3. ya viene todo puesto en requeriments.txt, entonces ```pip install -r requirements.txt``` para descargar todas las dependencias, aunque solo usamos ```pyodbc```, ```Flask``` y ```waitress```.

### Configuración
1. MS SQL Server instalado, claramente también el management studio.

2. [Descargar ODBC driver](https://learn.microsoft.com/es-es/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16)  para facilitar la conexión entre el programa y la base, de preferencia la versión 18.

3. Creamos la base, las consultas ya están en ```tablesQuerys.sql``` para no batallar.

4. En ```main.py```, especificamente linea 17 y 18, está el nombre del servidor y de la base, si tu servidor tiene otro nombre debes cambiarlo.

5. En la linea 20, si tu servidor requiere usuario y contraseña debes sustituir la parte de ```trusted_connection=yes``` con dichos datos.
### Ejecutar
Teoricamente todo se encuentra en orden, solo bastaría ejecutar dentro de la carpeta ```waitress-serve --port=8000 main:app``` para que la aplicación se inicie en localhost:8000.
Si por alguna razón tienes interés en iniciarla desde el servidor de desarrollo, aunque es significativamente más lento, se haría con ```flask --app main run``` o ```py main.py``` en caso de tener el debug activado

## Endpoints guide
### main.py
Todas las rutas aquí descritas devuelven HTML procesado con datos especificos, se podría decir que son las que el usuario ve comunmente. 
- **/** : ruta principal, devuelve la página de presentación, hace consultas SQL para obtener los productos destacados.
- **/register** : Página de formulario donde el usuario se registra. Envía una petición a **/Register-new-user**.
- **/login** : Donde el usuario inicia sesión. La petición de inicio de sesión es enviada a si mismo.
- **/product/<id_product>** : dependiendo de ```id_product```, hace una consulta y carga un HTMl procesado.

- **/user** : carga la página de usuario dependiendo de la sesión.
- **/admin** : carga la página de administrador.
- **/search/<search_term>** : dependiendo de ```search_term``` carga una página de resultados de busqueda.
- **/cart** : muestra la página del carrito.
- **/update-user** : muestra el formulario para actualizar usuario.
- **/logout** : ruta para cerrar sesión. Redirige a **/**, pero con la sesión cerrada.
### postEp.py
Todas las rutas que reciben peticiones POST, devuelven JSON o redirecciones.
- **/register-new-user** : Agrega un usuario a la base de datos. Redirige a **/**.

- **/post-a-review/<id_product>** : Postea una reseña en ```id_product```.
- **/search-p** : Recibe una petición realizada por la barra de busqueda, procesa el término a buscar y redirige a **/search**.
- **/save-product/<id_product>** : guarda ```id_product``` en la cuenta del usuario.
- **/upload_product** : válida si la petición la hace el administrador, en caso de que si, sube un producto a la base de datos.
- **/c-theme** : cambia el tema (oscuro, claro) del usuario en la base de datos.
- **/add-cart** : Agrega un producto al carrito.
- **/del-cart** : Elimina un producto del carrito.
- **/delete-product** : Borra un producto de la base de datos si eres administrador.
- **/top-products** : Recibe una petición para cambiar los productos destacados.
- **/update-user-api** : Recibe una petición para cambiar los datos de un usuario en la base de datos.