import pyodbc

server = '(localdb)\\MainServer'  # e.g., 'localhost', 'my_server'
database = 'UsersWebP'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# Establecer la conexión
try:
    conn = pyodbc.connect(conn_str)
    print("Conexión exitosa")
    
    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()
    
    # Por ejemplo, ejecutar una consulta
    cursor.execute("SELECT * FROM users")
    
    # Recuperar y mostrar los resultados
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
    # Cerrar la conexión
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Error al conectar a SQL Server: {e}")