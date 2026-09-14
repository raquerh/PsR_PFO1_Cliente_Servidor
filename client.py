# PFO1 - Cliente del chat basico con sockets
# Programacion sobre Redes - IFTS29

import socket

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024
PALABRA_SALIDA = 'éxito'


def conectar_al_servidor():
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((HOST, PORT))
        print(f"Conectado al servidor {HOST}:{PORT}")
        return cliente_socket
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. ¿Esta corriendo?")
        return None


def main():
    cliente_socket = conectar_al_servidor()
    if cliente_socket is None:
        return

    print(f"Escribi tus mensajes. Escribi '{PALABRA_SALIDA}' para salir.\n")

    with cliente_socket:
        while True:
            mensaje = input('Vos: ')
            cliente_socket.sendall(mensaje.encode('utf-8'))

            respuesta = cliente_socket.recv(BUFFER_SIZE)
            print(f"Servidor: {respuesta.decode('utf-8')}")

            if mensaje.strip().lower() == PALABRA_SALIDA:
                break


if __name__ == '__main__':
    main()
