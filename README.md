# PsR_PFO1_Cliente_Servidor

Chat básico cliente-servidor en Python con sockets TCP y una base de datos SQLite, para la Practica Formativa Obligatoria 1 de Programacion sobre Redes.
Tecnicatura superior en desarrollo de software - IFTS29.

## Objetivo

Configurar un servidor de sockets que reciba mensajes de clientes, los guarde en una base de datos y envíe confirmaciones, aplicando modularización y manejo de errores.

## Archivos

- `server.py`: servidor TCP que escucha en `localhost:5000`, recibe mensajes y los guarda en SQLite.
- `client.py`: cliente de consola que se conecta al servidor y envía mensajes hasta que el usuario escribe `salir`.
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
3. Escribir mensajes en la terminal del cliente. Escribir `salir` para cortar la conexión.

Se puede abrir más de una terminal con `client.py` en simultáneo; el servidor atiende a cada cliente en un hilo aparte.

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

El servidor atiende cada conexión entrante en un hilo (`threading.Thread`) separado, así puede recibir mensajes de varios clientes en simultáneo. Como todos los hilos comparten la misma conexión a la base de datos, el acceso a `mensajes.db` está protegido con un `threading.Lock()` para evitar condiciones de carrera al escribir.