
# PFO1 - CHAT BASICO CLIENTE SERVIDOR



import socket
import sqlite3
import threading
from datetime import datetime

HOST = 'localhost'
PORT = 5000
DB_PATH = 'mensajes.db'
BUFFER_SIZE = 1024

def inicializar_socket(host=HOST, port=PORT):
    # Configuración del socket TCP/IP
    try:
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #(direcciones IPv4,TCP)
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor_socket.bind((host, port)) # bind asocia el socket a la direccion y puerto
        servidor_socket.listen()
        print(f"[SERVIDOR] Escuchando en {host}:{port}...")
        return servidor_socket
    except OSError as error:
        print(f"[SERVIDOR] No se pudo iniciar el socket en {host}:{port} -> {error}")
        raise

def inicializar_db(db_path=DB_PATH):
    try:
        conexion = sqlite3.connect(db_path, check_same_thread=False) # (necesario porque distintos hilos, uno por cliente, van a usar la misma conexion)
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)
        conexion.commit()
        print(f"[DB] Base de datos lista en '{db_path}'.")
        return conexion
    except sqlite3.Error as error:
        print(f"[DB] Error al inicializar la base de datos: {error}")
        raise
    
