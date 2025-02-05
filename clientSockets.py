import socket

#******* Clase de socket *******#
class MessageSocket:
    MSGLEN = 1024
    #******* Constructor de clase *******#
    def __init__(self, usrname:str, host:str, port:int)->None:
        #instancias
        self._username = usrname
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #******* Metodos de instancia *******#
    def connect(self)->None:
        #conexion del socket
        self._socket.connect((self._host, self._port))
    
    def send(self, msg):
        #cursor para mandar caracter a caracter
        cursor = 0
        
        #ciclo de mandado
        while cursor < len(msg):
            sent = self._socket.send(msg[cursor:])
            #validacion de enviado
            if sent == 0:
                break
            cursor = cursor + sent
    
    def recive(self)->str:
        return self._socket.recv(1024).decode()
    
    def close(self)->None:
        print("Conexion cerrada!!!!!")
        self._socket.close()
    #******* Metodos de atributo *******#
    def getUserName(self)->str:
        return self._username