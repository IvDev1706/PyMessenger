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
        texto = self._soc.getUserName()+': '+texto
        #se lo enviamos al servidor
        self._soc.send(texto.encode())
        #limpiamos la prompt
        self._chatPrompt.setText('')
        #pegamos el mensaje al chatView
        self._chatView.setText(self._chatView.text()+texto+'\n')
    
    #sobreescritura del metodp
    def closeEvent(self, event)->None:
        #cerrar la conexion socket
        self._soc.close()
    
    def connectServer(self)->None:
        #ventana emergente
        ip, _ = QInputDialog.getText(self,"Conexion a servidor","Ingrese la direccion ip del servidor:")
        user, _ = QInputDialog.getText(self, "Nombre de usuario", "Ingrese su nombre de usuario:")
        
        try:
            #instancia de socket y conexion
            self._soc = MessageSocket(user,ip,8000)
            self._soc.connect()
            self._soc.send(f"{self._soc.getUserName()} se ha unido al chat".encode())
            QMessageBox.information(self,"Conexion establecida","Se ha conectado al servidor!!",QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
            hilo = Thread(target=updateChat,args=(self._soc, self._chatView))
            hilo.start()
        except ConnectionRefusedError:
            QMessageBox.warning(self,"Conexion no establecida","El servidor rechazo la conexion o no esta activo",QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)

def updateChat(soc, chatView)->None:
        #ciclo de actualizacion
        while True:
            try:
                texto = soc.recive()
                if texto != 'v@':
                    chatView.setText(chatView.text()+texto+'\n')
            except ConnectionAbortedError:
                break

#******* Zona de lanzamiento *******#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    messenger = ClientMessenger()
    messenger.show()
    messenger.connectServer()
    sys.exit(app.exec())