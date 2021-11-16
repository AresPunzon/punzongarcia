'''
Fichero de eventos generales
'''
import os.path
import pathlib
import shutil
import sys, var, shutil
import zipfile
import xlrd

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtPrintSupport

import conexion
from ventana import *
from datetime import date, datetime
from zipfile import ZipFile

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
            for i in range(5):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 0 or i == 3:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        except Exception as error:
            print('Error al redimensionar la tabla ', error)

    def Abrir(self):
        try:
            var.dlgabrir.show()
        except Exception as error:
            print('Error al abrir cuadro diálogo ', error)

    def Backup(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha + '_backup.zip'))
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Guardar Copia', var.copia, '.zip', options = option)
            if var.dlgabrir.Accepted and filename != '':
                fichzip = zipfile.ZipFile(var.copia, 'w')
                fichzip.write(var.filedb, os.path.basename(var.filedb), zipfile.ZIP_DEFLATED)
                fichzip.close()

                msgBox = QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setMinimumSize(1024, 1024)  # no hace nada
                msgBox.setWindowTitle('Aviso Backup')
                msgBox.setText("Copia de seguridad creada")
                msgBox.exec()

                shutil.move(str(var.copia), str(directorio))
        except Exception as error:
            print('Error al hacer backup ', error)

    def Restaurar(self):
        try:
            dirpro = os.getcwd()
            print(dirpro)
            option = QtWidgets.QFileDialog.Options()
            filename = var.dlgabrir.getOpenFileName(None, 'Restaurar Copia de Seguridad', "", '*.zip;;All ', options=option)
            if var.dlgabrir.Accepted and filename != "":
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as pepe:
                    pepe.extractall(pwd = None)
                pepe.close()
                #shutil.move('pepe.sqlite', str(dirpro))
            conexion.Conexion.db_connect(var.filedb)
            conexion.Conexion.cargarTabCli(self)

        except Exception as error:
            print('Error al restaurar la base de datos ', error)

    def Imprimir(self):
        try:
            printDialog = QtWidgets.QFileDialog()
            if printDialog.exec_():
                printDialog.show()
        except Exception as error:
            print('Error al imprimir ', error)

    def ImportarDatos(self):
        try:
            documento = xlrd.open_workbook("DATOSCLIENTES.xls")
            clientes = documento.sheet_by_index(0)
            filas_clientes = clientes.nrows
            columnas_clientes = clientes.ncols
            print("Filas: " + str(filas_clientes) + ". Columnas: " + str(columnas_clientes))

            dirpro = os.getcwd()
            print(dirpro)
            option = QtWidgets.QFileDialog.Options()
            filename = var.dlgabrir.getOpenFileName(None, 'Cargar datos desde Excel', "", '*.xls;;All ',options=option)
        except Exception as error:
            print('Error al cargar datos del excel ', error)








