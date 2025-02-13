# PyMessenger
Pequeña aplicacion de mensajeria con sockets en python

## Programas
Los programas que contiene la aplicacion son los siguientes:
- Servidor (consola)
- Cliente (UI)

## Herramientas
Las herramientas (bibliotecas) empleadas son las siguientes:
- socket (python)
- PyQt6
- threading (python)

## Guia de uso
Para ejecutar la aplicacion se tiene que ejecutar primero el servidor en un equipo y despues
los clientes que puedne serv en diferentes equipos o en el mismo, actualmente soporta conexiones
LAN, WLAN y Local.

### Mensajes
Los mensajes son texto plano que simplemente se envia y se reenvia entre usuarios sin procesar.

### Comandos
Los comandos se denotan por C\command y son procesados por el cliente.

### Peticiones
Las peticiones se denotan por P\request y son procesadas por el servidor y este mismo
responde al usuario solicitante.
