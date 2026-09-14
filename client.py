import socket

HOST = "localhost"
PORT = 5000
BUFFER_SIZE = 1024
PALABRA_SALIDA = "salir"


def conectar_al_servidor(host=HOST, port=PORT):
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((host, port))
        print(f"[CLIENTE] Conectado al servidor {host}:{port}")
        return cliente_socket
    except ConnectionRefusedError:
        print(f"[CLIENTE] No se pudo conectar a {host}:{port}. ¿Esta el servidor corriendo?")
        return None


def enviar_mensajes(cliente_socket):
    print(f"Escribi tus mensajes. Escribi '{PALABRA_SALIDA}' para cortar la conexion.\n")

    while True:
        mensaje = input("Vos: ")

        try:
            cliente_socket.sendall(mensaje.encode("utf-8"))
        except (BrokenPipeError, ConnectionResetError):
            print("[CLIENTE] Se perdio la conexion con el servidor.")
            break

        try:
            respuesta = cliente_socket.recv(BUFFER_SIZE)
            if not respuesta:
                print("[CLIENTE] El servidor cerro la conexion.")
                break
            print(f"Servidor: {respuesta.decode('utf-8')}")
        except (ConnectionResetError, OSError) as error:
            print(f"[CLIENTE] Error al recibir la respuesta: {error}")
            break

        if mensaje.strip().lower() == PALABRA_SALIDA:
            print("[CLIENTE] Cerrando la conexion...")
            break

def main():
    cliente_socket = conectar_al_servidor()
    if cliente_socket is None:
        return

    with cliente_socket:
        enviar_mensajes(cliente_socket)


if __name__ == "__main__":
    main()