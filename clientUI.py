from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget, QLabel, QGridLayout, QApplication, QMessageBox
from PyQt6.QtCore import Qt
import sys
from clientSockets import MessageSocket
from threading import Thread

#clase de ventana
class ClientMessenger(QWidget):
    #******* COnstrutor de clase *******#
    def __init__(self)->None:
        #componentes
        super().__init__()
        self._chatView = QLabel()
        self._chatPrompt = QLineEdit()
        self._btnSend = QPushButton()
        self._lblserver = QLabel()
        self._lblport = QLabel()
        self._lblUser = QLabel()
        self._campoServer = QLineEdit()
        self._campoPort = QLineEdit()
        self._campoUser = QLineEdit()
        self._btnConnect = QPushButton()
        
        #socket de conexion
        self._soc = None
        
        #metodos de ventana
        self.__config()
        self.__build()
        self.__listen()
    #******* Metodos de ventana *******#
    def __config(self)->None:
        #configuracion de ventana
        self.setWindowTitle("PyMessenger")
        self.setFixedSize(500,400)
        
        #configuracion de componentes
        self._chatView.setText("Chats!!!\n")
        self._chatView.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._btnSend.setText("enviar")
        self._lblserver.setText("Ip de servidor:")
        self._lblport.setText("Puerto del servidor:")
        self._lblUser.setText("Nombre de usuario:")
        self._btnConnect.setText("conectar")
        self._campoServer.setFixedWidth(150)
        self._campoPort.setFixedWidth(150)
        self._campoUser.setFixedWidth(150)
        
    def __build(self)->None:
        #armado de la vista
        #panel de configuracion
        gLayout = QGridLayout()
        gLayout.addWidget(self._lblserver,0,0)
        gLayout.addWidget(self._campoServer,1,0)
        gLayout.addWidget(self._lblport,2,0)
        gLayout.addWidget(self._campoPort,3,0)
        gLayout.addWidget(self._lblUser,4,0)
        gLayout.addWidget(self._campoUser,5,0)
        gLayout.addWidget(self._btnConnect,6,0)
        
        #panel de chat
        gLayout.addWidget(self._chatView,0,1,6,3)
        gLayout.addWidget(self._chatPrompt,6,1,1,2)
        gLayout.addWidget(self._btnSend,6,3)
        
        #adicion a la ventana
        self.setLayout(gLayout)
    
    def __listen(self)->None:
        #esucha del boton de enviar
        self._btnSend.clicked.connect(self.__sendMessage)
        self._btnConnect.clicked.connect(self.__connectServer)
        
    def __sendMessage(self)->None:
        #obtener el texto del prompt
        texto = self._chatPrompt.text()
        
        #validar que no sea comando
        if not texto.startswith("C\\"):
            instruccion = 'e@--'+self._soc.getUserName()+'--m@--'+texto+"--s@--0"
            log = self._soc.getUserName()+': '+texto
            #se lo enviamos al servidor
            self._soc.send(instruccion.encode())
            #limpiamos la prompt
            self._chatPrompt.setText('')
            #pegamos el mensaje al chatView
            self._chatView.setText(self._chatView.text()+log+'\n')
        else:
            #interptretacion del comando
            if texto == "C\\exit":
                self.close()
            elif texto =="C\\bye":
                if self._soc != None:
                    self._soc.close()
                    self._chatPrompt.setText('')
                    QMessageBox.information(self,"Conexion cerrada","Has dejado la sala!!",QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
                else:
                    self._chatPrompt.setText('')
            else:
                self._chatPrompt.setText('')
                QMessageBox.warning(self,"Comando invalido","El comando ingresado es invalido!!",QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
                
            
    #sobreescritura del metodp
    def closeEvent(self, event)->None:
        #cerrar la conexion socket
        if self._soc != None:
            self._soc.close()
    
    def __connectServer(self)->None:
        #ventana emergente
        ip = self._campoServer.text() if self._campoServer.text() != "" else "127.0.0.1"
        port = int(self._campoPort.text())
        user = self._campoUser.text()
        
        try:
            #instancia de socket y conexion
            self._soc = MessageSocket(user,ip if ip != '' else '127.0.0.1',int(port))
            self._soc.connect()
            self._soc.send(f"e@--{self._soc.getUserName()}--m@--{self._soc.getUserName()} se ha unido al chat--s@--0".encode())
            QMessageBox.information(self,"Conexion establecida","Se ha conectado al servidor!!",QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
            hilo = Thread(target=updateChat,args=(self._soc, self._chatView))
            hilo.start()
        except ConnectionRefusedError:
            QMessageBox.warning(self,"Conexion no establecida","El servidor rechazo la conexion o no esta activo",QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)

def updateChat(soc, chatView)->None:
        #ciclo de actualizacion
        while True:
            try:
                inst = soc.recive()
                if inst != 'v@':
                    data = inst.split('--')
                    chatView.setText(chatView.text()+data[1]+': '+data[3]+'\n')
            except ConnectionAbortedError:
                break

#******* Zona de lanzamiento *******#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    messenger = ClientMessenger()
    messenger.show()
    sys.exit(app.exec())