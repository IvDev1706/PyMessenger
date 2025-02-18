import socket
import psutil
import threading

#******* Clase de servidor socket *******#
class ServerSocket:
    #******* Constructor de clase *******#
    def __init__(self)->None:
        #instancias
        self._port = 0
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socs = 0
        self._clients = []
        
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
    
    def __resend(self, addr, msg, room):
        for cliente in self._clients:
            if addr != cliente[0]:
                if room == cliente[3]:
                    cliente[1].sendall(msg)
    
    def __handleclient(self, conn, addr, drop_client, resend):
        #ciclo de recepcion y envio
        while True:
            try:
                #recibe los bytes
                msg = conn.recv(1024)
                #condicion de paro
                if not msg:
                    print(f"Cliente {addr} se desconecto")
                    #sacar al cliente de la lista
                    drop_client(addr)
                    break
                #filtrado de instruccion
                inst = msg.decode()
                data = inst.split('--')
                if data[2] == 'p@':
                    #comandos de servidor
                    if 'P\\join' in data[3]:
                        room = data[3].split(' ')[1]
                        for cliente in self._clients:
                            if cliente[0] == addr:
                                cliente[3] = room
                                break
                        #reenvio de mensaje de cambio
                        conn.sendall(f"e@--Server--m@--Te has cambiado a la sala {room}--s@--{room}".encode())
                    elif 'P\\address':
                        for cliente in self._clients:
                            if addr in cliente:
                                conn.sendall(f"e@--Server--m@--Tu direccion es: {cliente[0]}--s@--{cliente[3]}".encode())
                                break
                    elif 'P\\serverip':
                        for cliente in self._clients:
                            if addr in cliente:
                                conn.sendall(f"e@--Server--m@--Ipv4 (WLAN) del servidor ({self._serverIp})--s@--{cliente[3]}".encode())
                                break
                    elif 'P\\serverport':
                        for cliente in self._clients:
                            if addr in cliente:
                                conn.sendall(f"e@--Server--m@--Puerto del servidor ({self._serverIp})--s@--{cliente[3]}".encode())
                                break
                else:
                    #manda el mensaje a todos los clientes
                    resend(addr,msg,data[5])
            except socket.timeout:
                conn.send('v@'.encode())
            except ConnectionResetError:
                #eliminar de la lista al cliente
                print(f"Cliente {addr} se desconecto")
                drop_client(addr)
                break
    
    def start(self)->None:
        #mensajes de bienvenida e info del servidor
        print("<<-- PyMessenger Server -->>")
        print("****************************")
        print("Ingrese el numero de puerto:")
        self._port= int(input(">> "))
        print("Ingrese los clientes maximos:")
        self._socs = int(input(">> "))
        print("Servidor configurado!!!!!")
        print("****************************")
        #configuracion del servidor
        self._socket.bind(('',self._port))
        self._socket.listen(self._socs)
    
    def run(self)->None:
        self._serverIp = self.__getIpAddress()
        #info del servidor
        print(f"Direccion IP WLAN: {self._serverIp}")
        print(f"Puerto de servicio: {self._port}")
        print("Consola:")
        #ciclo de vida
        while True:
            #aceptar la conexion
            conn, addr = self._socket.accept()
            conn.settimeout(1.0)
            print(f"Conexion establecida con {addr}")
            #guardamos los clientes que entrar
            inst = conn.recv(1024).decode()
            data = inst.split('--')
            self._clients.append([addr,conn,data[1],data[5]])
            
            #reenvio de mensaje de union
            self.__resend(addr,inst.encode(),data[5])
            
            #hilos de cliente
            hilo_cliente = threading.Thread(target=self.__handleclient,args=(conn,addr,self.__drop_client,self.__resend))
            hilo_cliente.start()
        
# Ejecutar el servidor
if __name__ == "__main__":
    server = ServerSocket()
    server.start()#configura los valores
    server.run()#inicia el servicio