import sqlite3

# Muestra todos los mensajes guardados en la base de datos
conexion = sqlite3.connect("mensajes.db")
for fila in conexion.execute("SELECT * FROM mensajes"):
    print(fila)
conexion.close()