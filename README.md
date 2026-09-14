# PsR_PFO1_Cliente_Servidor

Chat básico cliente-servidor en Python con sockets TCP y una base de datos SQLite, para la Practica Formativa Obligatoria 1 de Programacion sobre Redes. Tecnicatura superior en desarrollo de software - IFTS29.

## Objetivo

Configurar un servidor de sockets que reciba mensajes de clientes, los guarde en una base de datos y envíe confirmaciones, aplicando modularización y manejo de errores.

## Archivos

- `server.py`: servidor TCP que escucha en `localhost:5000`, recibe mensajes y los guarda en SQLite.
- `client.py`: cliente de consola que se conecta al servidor y envía mensajes hasta que el usuario escribe `éxito`.
- `TestMensajesDB.py`: script chico para revisar el contenido de la base de datos (imprime todas las filas de la tabla `mensajes`).
- `mensajes.db`: base de datos SQLite (se crea sola la primera vez que se corre el servidor).

## Requisitos

Python 3, sin dependencias externas: `socket`, `sqlite3`, `threading` y `datetime` son de la librería estándar.

## Cómo correrlo

1. En una terminal, dentro de la carpeta del proyecto:
   ```
   python3 server.py
   ```
2. En otra terminal:
   ```
   python3 client.py
   ```
3. Escribir mensajes en la terminal del cliente. Escribir `éxito` para cortar la conexión.

El servidor atiende a un cliente a la vez; si abrís otra terminal con `client.py` mientras la primera sigue conectada, va a quedar esperando hasta que la primera se desconecte.

## Base de datos

La tabla `mensajes` se crea automáticamente al iniciar el servidor, con los campos:

| Campo | Tipo | Descripción |
|---|---|---|
| id | INTEGER | autoincremental |
| contenido | TEXT | texto del mensaje |
| fecha_envio | TEXT | timestamp en que se guardó |
| ip_cliente | TEXT | IP de origen del cliente |

Para revisar el contenido, correr:
```
python3 TestMensajesDB.py
```

## Manejo de errores

- Puerto ocupado al iniciar el socket del servidor.
- Base de datos no accesible al iniciar SQLite.
- Desconexión abrupta del cliente durante el envío o la recepción de datos.

## Notas de implementación

El servidor atiende un cliente a la vez: recién vuelve a llamar a `accept()` cuando el cliente anterior cierra la conexión.
