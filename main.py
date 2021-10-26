import PyQt5.uic.uiparser

import clients
import conexion
from aviso import *
from ventana import *
from windowCal import *
import sys, var
import events
from datetime import *

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        '''
        clase calendario
        '''
        super(DialogCalendar, self).__init__()
        var.dlgCalendar = Ui_windowCal()
        var.dlgCalendar.setupUi(self)
        diactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgCalendar.calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diactual)))
        var.dlgCalendar.calendar.clicked.connect(clients.Clientes.cargarFecha)

class DialogAviso(QtWidgets.QDialog):
    '''
    si da error añadir esto en aviso.py

    self.btnboxaviso.accepted.connect(aviso.accept)
    self.btnboxaviso.rejected.connect(aviso.reject)
    '''

    def __init__(self):
        super(DialogAviso, self).__init__()
        var.dlgaviso = Ui_aviso()
        var.dlgaviso.setupUi(self)
        # Otra manera de solucionar el error sin hacer el copia-pega
        var.dlgaviso.btnboxaviso.accepted.connect(self.accept)
        var.dlgaviso.btnboxaviso.rejected.connect(self.reject)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_MainWindow()
        var.ui.setupUi(self)
        '''
        Eventos de botón
        '''
        var.ui.btnsalir.clicked.connect(events.Eventos.Salida)
        var.ui.rbtGroupSex.buttonClicked.connect(clients.Clientes.setSexo)
        var.ui.chGroupPago.buttonClicked.connect(clients.Clientes.setPago)
        var.ui.btnCalendar.clicked.connect(events.Eventos.abrirCal)
        var.ui.btnGrabaCli.clicked.connect(clients.Clientes.guardaCli)
        var.ui.btnLimpiaFormCli.clicked.connect(clients.Clientes.limpiarForm)
        '''
        Eventos de la barra de menús
        '''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salida)
        '''
        Eventos caja de tecxto
        '''
        var.ui.txtdni.editingFinished.connect(clients.Clientes.validarDNI)
        var.ui.txtNome.editingFinished.connect(clients.Clientes.mayuscNome)
        var.ui.txtApe.editingFinished.connect(clients.Clientes.mayuscApe)
        var.ui.txtDir.editingFinished.connect(clients.Clientes.mayuscDir)
        '''
        Eventos de comboBox
        '''
        clients.Clientes.cargaProv(self)
        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        clients.Clientes.cargaMuni(self)
        var.ui.cmbMuni.activated[str].connect(clients.Clientes.selMuni)
        '''
        Eventos QTwidget
        '''
        events.Eventos.resizeTablaCli(self)
        var.ui.tabCliente.clicked.connect(clients.Clientes.cargaCli)
        var.ui.tabCliente.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        '''
        Base de datos
        '''
        conexion.Conexion.db_connect(var.filedb)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ventana = Main()
    var.dlgaviso = DialogAviso()
    var.dlgCalendar = DialogCalendar()
    ventana.show()
    sys.exit(app.exec())
