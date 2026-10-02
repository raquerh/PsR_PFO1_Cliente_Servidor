# PsR_PFO1_Cliente_Servidor

Chat básico cliente-servidor en Python con sockets TCP y una base de datos SQLite, para la Propuesta Formativa Obligatoria 1 de Programación sobre Redes. Tecnicatura Superior en Desarrollo de Software, IFTS 29, 2026.

## Objetivo

Configurar un servidor de sockets que reciba mensajes de clientes, los guarde en una base de datos y envíe confirmaciones, aplicando modularización y manejo de errores.

## Archivos

- `server.py`: servidor TCP que escucha en `localhost:5000`, recibe mensajes, los guarda en SQLite y responde con una confirmación.
- `client.py`: cliente de consola que se conecta al servidor y envía mensajes hasta que el usuario escribe `éxito`.
- `TestMensajesDB.py`: script para revisar la base de datos; imprime todas las filas de la tabla `mensajes`.
- `mensajes.db`: base de datos SQLite. Si no existe, el servidor la crea al iniciar.

## Requisitos

Python 3. No hace falta instalar nada: `socket`, `sqlite3` y `datetime` son de la librería estándar.

## Cómo correrlo

1. En una terminal, dentro de la carpeta del proyecto:
   ```
   python3 server.py
   ```
2. En otra terminal:
   ```
   python3 client.py
   ```
3. Escribir mensajes en la terminal del cliente. Por cada mensaje, el servidor responde `Mensaje recibido: <fecha y hora>`.
4. Escribir `éxito` para cortar la conexión. Ese último mensaje también se envía y se guarda.
5. Para apagar el servidor, Ctrl+C en su terminal.

## Servidor

`server.py` está dividido en funciones:

- `inicializar_socket()`: crea el socket TCP/IP (`AF_INET`, `SOCK_STREAM`), lo vincula a `localhost:5000` con `bind()` y lo pone a escuchar con `listen()`.
- `inicializar_db()`: abre `mensajes.db` y crea la tabla `mensajes` si no existe.
- `guardar_mensaje()`: inserta el mensaje con la fecha y hora actual y la IP del cliente, y devuelve la fecha para usarla en la respuesta.
- `recibir_mensajes()`: recibe los mensajes de un cliente, los guarda y le responde a cada uno, hasta que el cliente cierra la conexión.
- `main()`: inicializa la base y el socket, y queda aceptando conexiones con `accept()`.

Los mensajes se reciben de a 1024 bytes y se decodifican como UTF-8.

## Base de datos

La tabla `mensajes` tiene estos campos:

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | clave primaria autoincremental |
| contenido | TEXT | texto del mensaje |
| fecha_envio | TEXT | fecha y hora en que se guardó, formato `AAAA-MM-DD HH:MM:SS` |
| ip_cliente | TEXT | IP de origen del cliente |

El `INSERT` usa parámetros (`?`) en lugar de armar la consulta con el texto del mensaje.

Para revisar el contenido:
```
python3 TestMensajesDB.py
```

## Manejo de errores

Servidor:

- Puerto ocupado al iniciar el socket (`OSError`): muestra el error, cierra la base y termina.
- Base de datos no accesible (`sqlite3.Error`): muestra el error y termina sin levantar el socket.
- Cierre del cliente: cuando `recv()` devuelve vacío, el servidor cierra esa conexión y vuelve a esperar otro cliente.
- Ctrl+C (`KeyboardInterrupt`): apaga el servidor y cierra la base.

Cliente:

- Servidor no disponible (`ConnectionRefusedError`): avisa que no se pudo conectar y termina.

## Limitaciones conocidas

- El servidor atiende un cliente a la vez. Recién vuelve a llamar a `accept()` cuando el cliente anterior cierra la conexión; si se abre otro `client.py` mientras el primero sigue conectado, queda esperando.
- Si el cliente se cierra de golpe (por ejemplo, cerrando la terminal), `recv()` puede lanzar `ConnectionResetError`. Esa excepción no está capturada, así que el servidor se detiene.
- Si se envía un mensaje vacío (Enter sin escribir nada), no viaja ningún dato: el cliente queda esperando una respuesta que no llega y la conexión se traba.
- La palabra de salida no distingue mayúsculas (`éxito`, `Éxito` y `ÉXITO` funcionan igual), pero tiene que llevar tilde.
