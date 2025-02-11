from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QInputDialog, QMessageBox
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
        self.setFixedSize(400,300)
        
        #configuracion de componentes
        self._chatView.setText("Chats!!!\n")
        self._chatView.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._btnSend.setText("send")
        
    def __build(self)->None:
        #armado de la vista
        #panel de envio
        hLayout = QHBoxLayout()
        hLayout.addWidget(self._chatPrompt)
        hLayout.addWidget(self._btnSend)
        
        #panel principal
        vLayout = QVBoxLayout()
        vLayout.addWidget(self._chatView)
        vLayout.addLayout(hLayout)
        
        #adicion a la ventana
        self.setLayout(vLayout)
    
    def __listen(self)->None:
        #esucha del boton de enviar
        self._btnSend.clicked.connect(self.__sendMessage)
        
    def __sendMessage(self)->None:
        #obtener el texto del prompt
        texto = self._chatPrompt.text()
        instruccion = 'e@--'+self._soc.getUserName()+'--m@--'+texto+"--s@--0"
        log = self._soc.getUserName()+': '+texto
        #se lo enviamos al servidor
        self._soc.send(instruccion.encode())
        #limpiamos la prompt
        self._chatPrompt.setText('')
        #pegamos el mensaje al chatView
        self._chatView.setText(self._chatView.text()+log+'\n')
    
    #sobreescritura del metodp
    def closeEvent(self, event)->None:
        #cerrar la conexion socket
        self._soc.close()
    
    def connectServer(self)->None:
        #ventana emergente
        ip, _ = QInputDialog.getText(self,"Conexion a servidor","Ingrese la direccion ip del servidor:(127.0.0.1 por omision)")
        port, _ = QInputDialog.getText(self,"Puerto de servidor","Ingrese el puerto del servidor")
        user, _ = QInputDialog.getText(self, "Nombre de usuario", "Ingrese su nombre de usuario:")
        
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
    messenger.connectServer()
    sys.exit(app.exec())