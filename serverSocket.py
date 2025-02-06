import socket
import psutil
import threading

#******* Clase de servidor socket *******#
class ServerSocket:
    #******* Constructor de clase *******#
    def __init__(self, socs:int)->None:
        #instancias
        self._port = 8000
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socs = socs
        self._clients = []
        
        #configuracion del servidor
        self._socket.bind(('',self._port))
        self._socket.listen(self._socs)
        
    #******* Metodos de instancia *******#
    def __getIpAddress(self)->str:
        #iterar sobre los adaptadores de red
        for intf, addrs in psutil.net_if_addrs().items():
            #filtrado de adaptador wifi
            if "Wi-Fi" in intf or "wlan" in intf.lower():
                for addr in addrs:
                    #filtrado de la red de ip
                    if addr.family == socket.AF_INET:
                        return addr.address
                    
        return "No se encontró la IP del Wi-Fi"
    
    def __drop_client(self, addr):
        #iteramos por la lista de clientes
        for cliente in self._clients:
            #validamos que sea el cliente
            if addr in cliente:
                #eliminamo al cliente de la lista
                self._clients.remove(cliente)
                break
    
    def __handleclient(self, conn, addr, drop_client):
        #ciclo de recepcion y envio
        while True:
            try:
                #recibe los bytes
                msg = conn.recv(1024)
                #condicion de paro
                if not msg:
                    print(f"Cliente {addr} dejo de mandar datos")
                    #sacar al cliente de la lista
                    drop_client(addr)
                    break
                #manda el mensaje a todos los clientes
                print(msg.decode())
                """
                for cliente in self._clients:
                    addrC, connC = cliente
                    connC.sendall(msg)
                """
            except ConnectionResetError:
                #eliminar de la lista al cliente
                drop_client(addr)
                break
    
    def run(self)->None:
        #info del servidor
        print(f"Direccion del servidor: {self.__getIpAddress()}")
        print(f"Puerto del servidor: {self._port}")
        print("Conexiones:")
        
        #ciclo de vida
        while True:
            #aceptar la conexion
            conn, addr = self._socket.accept()
            print(f"Conexion establecida con {addr}")
            #guardamos los clientes que entrar
            self._clients.append((addr,conn))       
            
            #hilos de cliente
            hilo_cliente = threading.Thread(target=self.__handleclient,args=(conn,addr,self.__drop_client))
            hilo_cliente.start()
        
# Ejecutar el servidor
if __name__ == "__main__":
    server = ServerSocket(5)
    server.run()