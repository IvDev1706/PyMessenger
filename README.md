# PyMessenger
Pequeña aplicacion de mensajes con sockets en python

## Programas
los programas que conforman a la aplicacion son los siguientes:
- Servidor socket (terminal)
- Cliente (UI)

## Herramientas empleadas:
Las herramientas (bilbiotecas) empleadas son las siguientes:
- socket (python)
- PyQt6
- threading (python)

## Guia de uso
Para poder ejecutar la aplicacion se debe ejecutar el servidor primero en un equipo
despues se ejecuta el cliente, puede ser en diferentes equipos o local (del mismo equipo)
de momento solo soporta comunicacion via LAN, WLAN o Local.

### Mensajes
Los mensajes son texto plano que se envia y se reenvia netre los clientes y no es procesado.

### Comandos
Los comandos se denotan con C\command y estos son acciones que el cliente procesa.

### Peticiones
Las peticiones se denotan por P\request y estas son acciones que el servidor procesa y
reenvia al cliente.
