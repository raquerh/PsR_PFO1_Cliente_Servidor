# PFO1 - Chat basico cliente-servidor con sockets y SQLite
# Programacion sobre Redes - IFTS29

import socket
import sqlite3
from datetime import datetime

HOST = 'localhost'
PORT = 5000
DB_PATH = 'mensajes.db'
BUFFER_SIZE = 1024


def inicializar_socket():
    # Configuracion del socket TCP/IP
    try:
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket.bind((HOST, PORT))
        servidor_socket.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")
        return servidor_socket
    except OSError as error:
        print(f"No se pudo iniciar el servidor, puerto ocupado: {error}")
        raise


def inicializar_db():
    # Crea la base de datos y la tabla mensajes si no existen
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conexion.commit()
        return conexion
    except sqlite3.Error as error:
        print(f"No se pudo acceder a la base de datos: {error}")
        raise


def guardar_mensaje(conexion_db, contenido, ip_cliente):
    # Guarda el mensaje en la DB con la fecha y hora actual
    fecha_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = conexion_db.cursor()
    cursor.execute(
        "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
        (contenido, fecha_envio, ip_cliente)
    )
    conexion_db.commit()
    return fecha_envio


def recibir_mensajes(conexion_cliente, direccion, conexion_db):
    # Recibe los mensajes de un cliente hasta que corta la conexion
    ip_cliente = direccion[0]
    print(f"Cliente conectado: {direccion}")

    with conexion_cliente:
        while True:
            datos = conexion_cliente.recv(BUFFER_SIZE)
            if not datos:
                break  # el cliente cerro la conexion

            mensaje = datos.decode('utf-8')
            print(f"Mensaje de {ip_cliente}: {mensaje}")

            timestamp = guardar_mensaje(conexion_db, mensaje, ip_cliente)
            respuesta = f"Mensaje recibido: {timestamp}"
            conexion_cliente.sendall(respuesta.encode('utf-8'))

    print(f"Cliente desconectado: {direccion}")


def main():
    try:
        conexion_db = inicializar_db()
    except sqlite3.Error:
        return

    try:
        servidor_socket = inicializar_socket()
    except OSError:
        conexion_db.close()
        return

    try:
        with servidor_socket:
            while True:
                # Acepta conexiones y recibe los mensajes de cada cliente
                conexion_cliente, direccion = servidor_socket.accept()
                recibir_mensajes(conexion_cliente, direccion, conexion_db)
    except KeyboardInterrupt:
        print("\nApagando el servidor")
    finally:
        conexion_db.close()


if __name__ == '__main__':
    main()
