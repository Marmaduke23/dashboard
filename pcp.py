import pyodbc
drivers = pyodbc.drivers()
# Definir la cadena de conexión (ajusta estos valores)
server = '172DPRESIONES\\MSSQL2014'  # Dirección del servidor
database = 'nombre_base_datos'      # Nombre de la base de datos
username = 'consultaPresiones'      # Tu usuario
password = 'conPres025'                    # Tu contraseña

# Conectar a SQL Server usando pyodbc
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                      f'SERVER={server};'
                      f'UID={username};'
                      f'PWD={password};'
                      f'TrustServerCertificate=yes;')

cursor = conn.cursor()

#tabla = tblRegistro
#cursor.execute('SELECT * FROM INFORMATION_SCHEMA.TABLES;')

cursor.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'tblRegistro';")

# Recupera los resultados
columns = cursor.fetchall()

# Imprime las columnas
for column in columns:
    print(column)




