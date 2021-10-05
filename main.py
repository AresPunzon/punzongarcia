import PyQt5.uic.uiparser
from ventana import *
import sys

class Main(QtWidgets.QMainWindow):
        def __init__(self):
            super(Main, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ventana = Main()
    ventana.show()
    sys.exit(app.exec())
