
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
    
def guardar_mensaje(conexion_db, lock_db, contenido, ip_cliente):
    fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with lock_db: #evita que 2 hilos escriban al mismo tiempo en la base de datos
            cursor = conexion_db.cursor()
            cursor.execute(
                "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                (contenido, fecha_envio, ip_cliente)
            )
            conexion_db.commit()
        return fecha_envio
    except sqlite3.Error as error:
        print(f"[DB] Error al guardar el mensaje: {error}")
        return None

def manejar_cliente(conexion_cliente, direccion, conexion_db, lock_db):
    ip_cliente = direccion[0]
    print(f"[SERVIDOR] Cliente conectado desde {direccion}")

    try:
        with conexion_cliente:
            while True:
                datos = conexion_cliente.recv(BUFFER_SIZE) # recv espera los datos del cliente
                if not datos:
                    break  # el cliente cerró la conexión

                mensaje = datos.decode("utf-8").strip()
                print(f"[SERVIDOR] Mensaje de {ip_cliente}: {mensaje}")

                timestamp = guardar_mensaje(conexion_db, lock_db, mensaje, ip_cliente)

                if timestamp:
                    respuesta = f"Mensaje recibido: {timestamp}"
                else:
                    respuesta = "Error: no se pudo guardar el mensaje en la base de datos"

                conexion_cliente.sendall(respuesta.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError) as error:
        print(f"[SERVIDOR] Conexión perdida con {direccion}: {error}")
    finally:
        print(f"[SERVIDOR] Cliente {direccion} desconectado.")    
        
def main():
    try:
        conexion_db = inicializar_db()
    except sqlite3.Error:
        print("[SERVIDOR] No se pudo iniciar por un problema con la base de datos. Abortando.")
        return

    lock_db = threading.Lock()

    try:
        servidor_socket = inicializar_socket()
    except OSError:
        print("[SERVIDOR] No se pudo iniciar por un problema con el socket. Abortando.")
        conexion_db.close()
        return

    try:
        with servidor_socket:
            while True:
                conexion_cliente, direccion = servidor_socket.accept() # accept bloquea hasta que un cliente se conecta, devuelve un nuevo socket y la direccion del cliente
                hilo_cliente = threading.Thread(
                    target=manejar_cliente,
                    args=(conexion_cliente, direccion, conexion_db, lock_db),
                    daemon=True
                )
                hilo_cliente.start()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Apagando el servidor...")
    finally:
        conexion_db.close()


if __name__ == "__main__":
    main()