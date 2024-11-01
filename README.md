# Puntos impontantes por recordar
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
