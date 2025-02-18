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
        self._room = '0'
        self._connected = False
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #******* Metodos de instancia *******#
    def connect(self)->None:
        #conexion del socket
        self._socket.connect((self._host, self._port))
        self._connected = True
    
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
        return self._socket.recv(MessageSocket.MSGLEN).decode()
    
    def reborn(self)->None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def close(self)->None:
        print("Conexion cerrada!!!!!")
        self._connected = False
        self._socket.close()
    #******* Metodos de atributo *******#
    def getUserName(self)->str:
        return self._username
    
    def getRoom(self)->str:
        return self._room
    
    def setRoom(self, room:str)->None:
        self._room = room
        
    def isConnected(self)->bool:
        return self._connected