import none as none
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

import var
import conexion
from babel.numbers import format_currency
import locale
locale.setlocale( locale.LC_ALL, '' )

class Facturas():
    def buscaCli(self):
        try:
            dni = var.ui.txtDNIFac.text().upper()
            var.ui.txtDNIFac.setText(dni)
            registro = conexion.Conexion.buscaCliFac(dni)
            if registro:
                nombre = registro[0] + ", " + registro[1]
                var.ui.lblNomFac.setText(nombre)
                var.ui.lblNumFactura.setText("")
                var.ui.txtFechaFac.setText("")
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText("Cliente no existe")
                msgBox.setWindowTitle("No encontrado")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

        except Exception as error:
            print("Error al buscar cliente en las facturas ", error)

    def altaFac(self):
        try:
            registro = []
            dni = var.ui.txtDNIFac.text().upper()
            registro.append(str(dni))
            var.ui.txtDNIFac.setText(dni)
            fechaFac = var.ui.txtFechaFac.text()
            registro.append(str(fechaFac))
            conexion.Conexion.buscaCliFac(dni)
            conexion.Conexion.altaFac(registro)
            conexion.Conexion.cargaTabFacturas(self)
            codfac = conexion.Conexion.buscaCodFac(self)
            var.ui.lblNumFactura.setText(str(codfac))

        except Exception as error:
            print("Error alta en facturas ", error)

    def cargaFac(self):
        try:
            fila = var.ui.tabFacturas.selectedItems()
            datos = [var.ui.lblNumFactura, var.ui.txtFechaFac]
            if fila:
                row = [dato.text() for dato in fila]
            for i, dato in enumerate(datos):
                dato.setText(row[i])
            #aquí cargamos dni y nombre del cliente
            dni = conexion.Conexion.buscaDNIFac(row[0])
            var.ui.txtDNIFac.setText(str(dni))
            registro = conexion.Conexion.buscaCliFac(dni)
            if registro:
                nombre = registro[0] + ", " + registro[1]
                var.ui.lblNomFac.setText(nombre)
            conexion.Conexion.cargarLineasVenta(str(var.ui.lblNumFactura.text()))

        except Exception as error:
            print('Error al cargar datos de una factura ', error)

    # def cargarLineaVenta(self):
    #     try:
    #         index = 0
    #         var.cmbproducto = QtWidgets.QComboBox()
    #         #var.txtCantidad = QtWidgets.QLineEdit()
    #         #conexion.Conexion.cargarCmbProducto()
    #         var.cmbproducto.setFixedSize(150, 25)
    #         var.txtCantidad.setFixedSize(60, 25)
    #         var.txtCantidad.setAlignment(QtCore.Qt.AlignCenter)
    #         var.ui.tabVentas.setRowCount(index + 1)
    #         var.ui.tabVentas.setCellWidget(index, 1, var.cmbproducto)
    #         var.ui.tabVentas.setCellWidget(index, 3, var.txtCantidad)
    #     except Exception as error:
    #         print('Error al cargar linea venta ', error)

    def cargarLineaVenta(index):
        try:
            var.cmbproducto = QtWidgets.QComboBox()
            var.cmbproducto.currentIndexChanged.connect(Facturas.procesoVenta)
            var.cmbproducto.setFixedSize(170, 25)
            conexion.Conexion.cargarCmbProducto(self=None)
            var.txtCantidad = QtWidgets.QLineEdit()
            var.txtCantidad.editingFinished.connect(Facturas.totalLineaVenta)
            var.txtCantidad.setFixedSize(80, 25)
            var.txtCantidad.setAlignment(QtCore.Qt.AlignCenter)
            var.ui.tabVentas.setRowCount(index + 1)
            var.ui.tabVentas.setCellWidget(index, 1, var.cmbproducto)
            var.ui.tabVentas.setCellWidget(index, 3, var.txtCantidad)
        except Exception as error:
            print('Error al cargar linea venta ', error)

    def procesoVenta(self):
        try:
            if (var.cmbproducto.currentText() != ''):
                articulo = var.cmbproducto.currentText()
                dato = conexion.Conexion.obtenerPrecio(articulo)
                row = var.ui.tabVentas.currentRow()
                var.precio = dato[1]
                precioEu = format_currency(dato[1], 'EUR', locale='de_DE')
                var.codpro = dato[0]
                var.ui.tabVentas.setItem(row, 2, QtWidgets.QTableWidgetItem(str(precioEu)))
                #var.ui.tabVentas.setItem(row, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tabVentas.item(row, 2).setTextAlignment(QtCore.Qt.AlignCenter)

        except Exception as error:
            print('Error al procesar una venta ', error)

    def totalLineaVenta(self = None):
        try:
            venta = []
            row = var.ui.tabVentas.currentRow()
            cantidad = round(float(var.txtCantidad.text().replace(",", ".")), 2)
            totalLinea = round(float(var.precio) * float(cantidad), 2)
            var.ui.tabVentas.setItem(row, 4, QtWidgets.QTableWidgetItem(str(totalLinea) + '€'))
            var.ui.tabVentas.item(row, 4).setTextAlignment(QtCore.Qt.AlignRight)
            codfac = var.ui.lblNumFactura.text()
            venta.append(int(codfac))
            venta.append(int(var.codpro))
            venta.append((float(var.precio)))
            venta.append(float(cantidad))
            conexion.Conexion.cargarVenta(venta)

        except Exception as error:
            print('Error al procesar el total de una venta ', error)

    def limpiarFacturas(self):
        try:
            var.ui.txtDNIFac.setText("")
            var.ui.lblNumFactura.setText("")
            var.ui.txtFechaFac.setText("")
            var.ui.lblNomFac.setText("")
            conexion.Conexion.cargaTabFacturas(self)

        except Exception as error:
            print('Error al limpiar campos de factura ', error)












































