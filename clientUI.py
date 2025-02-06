from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QApplication, QInputDialog, QMessageBox
from PyQt6.QtCore import Qt
import sys
from clientSockets import MessageSocket

#clase de ventana
class ClientMessenger:
    #******* COnstrutor de clase *******#
    def __init__(self)->None:
        #componentes
        self._window = QWidget()
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
        self._window.setWindowTitle("PyMessenger")
        self._window.setFixedSize(400,300)
        
        #configuracion de componentes
        self._chatView.setText("Chats!!!")
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
        self._window.setLayout(vLayout)
    
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
    
    def connectServer(self)->None:
        #ventana emergente
        ip, _ = QInputDialog.getText(self._window,"Conexion a servidor","Ingrese la direccion ip del servidor:")
        user, _ = QInputDialog.getText(self._window, "Nombre de usuario", "Ingrese su nombre de usuario:")
        
        try:
            #instancia de socket y conexion
            self._soc = MessageSocket(user,ip,8000)
            self._soc.connect()
            QMessageBox.information(self._window,"Conexion establecida","Se ha conectado al servidor!!",QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)
        except ConnectionRefusedError:
            QMessageBox.warning(self._window,"Conexion no establecida","El servidor rechazo la conexion o no esta activo",QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.Ok)

    def show(self)->None:
        self._window.show()

#******* Zona de lanzamiento *******#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    messenger = ClientMessenger()
    messenger.show()
    messenger.connectServer()
    sys.exit(app.exec())