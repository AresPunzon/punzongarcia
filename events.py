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
from PyQt5 import QtPrintSupport, QtSql

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

    def resizeTablaArticulos(self):
        try:
            header = var.ui.tabProd.horizontalHeader()
            for i in range(3):
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
                if i == 0 or i == 2:
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
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Guardar Copia', var.copia, '.zip',
                                                                options=option)
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
            filename = var.dlgabrir.getOpenFileName(None, 'Restaurar Copia de Seguridad', "", '*.zip;;All ',
                                                    options=option)
            if var.dlgabrir.Accepted and filename != "":
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as pepe:
                    pepe.extractall(pwd=None)
                pepe.close()
                # shutil.move('pepe.sqlite', str(dirpro))
            conexion.Conexion.db_connect(var.filedb)
            conexion.Conexion.cargarTabCli(self)

        except Exception as error:
            print('Error al restaurar la base de datos ', error)

    def Imprimir(self):
        try:
            printDialog = QtPrintSupport.QPrintDialog()
            if printDialog.exec_():
                printDialog.show()
        except Exception as error:
            print('Error al imprimir ', error)

    def ImportarDatos(self):
        try:
            dirpro = os.getcwd()
            print(dirpro)
            option = QtWidgets.QFileDialog.Options()
            filename = var.dlgabrir.getOpenFileName(None, 'Cargar datos desde Excel', "", '*.xls;;All ', options=option)

            documento = xlrd.open_workbook(filename[0])
            clientes = documento.sheet_by_index(0)
            filas_clientes = clientes.nrows
            columnas_clientes = clientes.ncols
            print("Filas: " + str(filas_clientes) + ". Columnas: " + str(columnas_clientes))

            if var.dlgabrir.Accepted and filename != "":
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Confirmar')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('¿Estás seguro de seleccionar este archivo?')
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec()
                if msg.clickedButton() == msg.button(msg.StandardButton.Ok):
                    dnis = []
                    query = QtSql.QSqlQuery()
                    query.prepare('select dni from clientes')
                    if query.exec_():
                        while query.next():
                            dnis.append(query.value(0))

                    for i in range(clientes.nrows - 1):
                        c1 = clientes.cell_value(i + 1, 0)
                        c2 = clientes.cell_value(i + 1, 1)
                        c3 = clientes.cell_value(i + 1, 2)
                        c4 = clientes.cell_value(i + 1, 3)
                        c5 = clientes.cell_value(i + 1, 4)
                        c6 = clientes.cell_value(i + 1, 5)

                        if c1 in dnis:
                            query.prepare('update clientes set apellidos = :apellidos, nombre = :nombre, '
                                          'direccion = :direccion, provincia = :provincia, sexo = :sexo '
                                          'where dni = :dni')
                            query.bindValue(':dni', c1)
                            query.bindValue(':apellidos', c2)
                            query.bindValue(':nombre', c3)
                            query.bindValue(':direccion', c4)
                            query.bindValue(':provincia', c5)
                            query.bindValue(':sexo', c6)
                            query.exec()
                        else:
                            query.prepare(
                                'insert into clientes (dni, apellidos, nombre, direccion, provincia, sexo)'
                                'VALUES (:dni, :apellidos, :nombre, :direccion,:provincia, :sexo)')
                            query.bindValue(':dni', c1)
                            query.bindValue(':apellidos', c2)
                            query.bindValue(':nombre', c3)
                            query.bindValue(':direccion', c4)
                            query.bindValue(':provincia', c5)
                            query.bindValue(':sexo', c6)
                            query.exec()
                    conexion.Conexion.cargarTabCli(self)
                elif msg.clickedButton() == msg.button(msg.StandardButton.Cancel):
                    print("Importación cancelada")
        except Exception as error:
            print('Error al cargar datos del excel ', error)

    def ExportarDatos(self):
        try:
            conexion.Conexion.exportExcel(self)
            try:
                msgBox = QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText("Datos exportados con éxito.")
                msgBox.setWindowTitle("Operación completada")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
            except Exception as error:
                print('Error en mensaje generado exportar datos ', error)
        except Exception as error:
            print('Error en evento exportar datos ', error)
