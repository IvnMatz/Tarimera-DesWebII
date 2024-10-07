# Algunos puntos importantes
### instalación
debes tener en cuenta que si piensas descargar esto, debes tener lo siguiente instalado:
- Python: Obviamente
- Flask: hazlo con ``` pip install Flask ``` , aunque Flask recomienda hacerlo en un virtualenv
- pyodbc: igual, ``` pip install pyodbc ```
- MS SQL Server y ODBC: de preferencia las ultimas versiones de cada uno.
### configuración
Ahora para que el proyecto funcione correctamente, deberías tener configurado un servidor en localdb llamado "MainServer", y crear dentro una base de datos llamada UsersWebP (o cambiar los nombres en el codigo, lo que te sepa más conveniente) (El tema de las tablas me lo guardo porque me da flojera explicarlo).
Teoricamente, debería de estar todo correcto para funcionar con ```py main.py``` o ```flask --app main run```.
