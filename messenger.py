from clientSockets import MessageSocket
messageQueue = []
#capturamos la ip y el puerto del servidor
print("Ingrese la direccion ip del servidor:(127.0.0.1 por omision)")
host = input(">> ")
print('Ingrese el puerto del servidor: ')
port = int(input('>> '))
print('Ingrese su nombre de usuario: ')
usrname = input('>> ')
print("Conectando...")
try:
    #creamos el soceket
    soc = MessageSocket(usrname, host if host != '' else '127.0.0.1', port)
    soc.connect()
    #mensaje de union
    #soc.send(f"{soc.getUserName()} se ha unido al chat".encode())

    while True:
        #respuesta del servidor
        print(soc.recive())
        #el mensaje a enviar
        print('Mensaje a enviar')
        msg = input('>> ')
        #validacion de cierre
        if msg == 'terminar':
            break
        #enviar el mensaje
        msg = soc.getUserName()+': '+msg
        soc.send(msg.encode())
    soc.close()
except ConnectionRefusedError as e:
    print("El servidor rechazo la conexion o no esta activo")
except ConnectionResetError as e:
    print("Conexion con el servidor rota!!!!")