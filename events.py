'''

Fichero de eventos generales

'''
import sys
from ventana import *
import var

class Eventos():
    def Salida(self):
        try:
            var.dlgaviso.show()
            if var.dlgaviso.exec():
                sys.exit()
            else:
                var.dlgaviso.hide()
        except Exception as error:
            print('Error en módulo salir ', error)

    def abrirCal(self):
        try:
            var.dlgCalendar.show()
        except Exception as error:
            print('Error al abrir el calendario ', error)

    def resizeTablaCli(self):
        try:
            header = var.ui.tabCliente.horizontalHeader()
            for i in range(4):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as error:
            print('Error al redimensionar la tabla ', error)

