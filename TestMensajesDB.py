import sqlite3
conexion = sqlite3.connect("mensajes.db")
for fila in conexion.execute("SELECT * FROM mensajes"):
    print(fila)
conexion.close()