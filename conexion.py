from datetime import datetime

import xlwt as xlwt
from PyQt5 import QtSql, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

import conexion
import var
import locale
locale.setlocale( locale.LC_ALL, '' )

class Conexion:
    def db_connect(filedb):
        try:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filedb)
            if not db.open():
                QtWidgets.QMessageBox.critical(None,
                                               "No se puede abrir la base de alta.\n Haz clic para continuar",
                                               QtWidgets.QMessageBox.Cancel)
                return False
            else:
                print("Conexión establecida")
                return True
        except Exception as error:
            print('Problemas en la conexión', error)

    '''
    Módulos gestión DB clientes
    '''

    def altaCli(newCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into clientes (dni, alta, apellidos, nombre, direccion, provincia, municipio, sexo, pago, envio)'
                'VALUES (:dni, :alta, :apellidos, :nombre, :direccion,:provincia, :municipio, :sexo, :pago, :envio)')
            query.bindValue(':dni', str(newCli[0]))
            query.bindValue(':alta', str(newCli[1]))
            query.bindValue(':apellidos', str(newCli[2]))
            query.bindValue(':nombre', str(newCli[3]))
            query.bindValue(':direccion', str(newCli[4]))
            query.bindValue(':provincia', str(newCli[5]))
            query.bindValue(':municipio', str(newCli[6]))
            query.bindValue(':sexo', str(newCli[7]))
            query.bindValue(':pago', str(newCli[8]))
            query.bindValue(':envio', str(newCli[9]))

            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Cliente dado de Alta')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Problemas alta clientes', error)

    def cargarTabCli(self):
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare("select dni, apellidos, nombre, alta, pago from clientes order by apellidos")
            if query.exec_():
                while query.next():
                    dni = query.value(0)
                    apellidos = query.value(1)
                    nombre = query.value(2)
                    alta = query.value(3)
                    pago = query.value(4)
                    var.ui.tabCliente.setRowCount(index + 1)  # creamos la fila y cargamos datos
                    var.ui.tabCliente.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                    var.ui.tabCliente.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                    var.ui.tabCliente.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                    var.ui.tabCliente.setItem(index, 3, QtWidgets.QTableWidgetItem(alta))
                    var.ui.tabCliente.setItem(index, 4, QtWidgets.QTableWidgetItem(pago))
                    index += 1

        except Exception as error:
            print('Problemas en mostrar listado clientes', error)

    def oneClie(dni):
        try:
            record = []
            query = QtSql.QSqlQuery()
            query.prepare('select direccion, provincia, municipio, sexo, envio from clientes '
                          'where dni = :dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    for i in range(5):
                        record.append(query.value(i))
            return record
        except Exception as error:
            print('Problemas al mostrar datos de un cliente', error)

    def bajaCli(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from clientes where dni = :dni')
            query.bindValue(':dni', str(dni))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Cliente dado de baja')
                msg.exec()

        except Exception as error:
            print('Error baja cliente en conexión', error)

    def cargaProvCon(self):
        try:
            provId = []
            provNom = []
            prov = {}
            query = QtSql.QSqlQuery()
            query.prepare('select * from provincias')
            if query.exec_():
                while query.next():
                    provId.append(query.value(0))
                    provNom.append(query.value(1))
                prov = dict(zip(provId, provNom))
            return prov
        except Exception as error:
            print('Error en la selección de provincia', error)

    def cargaMuniCon(self):
        try:
            # busco el código de la provincia
            var.ui.cmbMuni.clear()
            prov = var.ui.cmbProv.currentText()
            query = QtSql.QSqlQuery()
            query.prepare('select id from provincias where provincia = :prov')
            query.bindValue(':prov', str(prov))
            if query.exec_():
                while query.next():
                    id = query.value(0)
            # cargo los municipios con ese código
            query1 = QtSql.QSqlQuery()
            query1.prepare('select municipio from municipios where provincia_id = :id')
            query1.bindValue(':id', int(id))
            if query1.exec_():
                var.ui.cmbMuni.addItem('')
                while query1.next():
                    var.ui.cmbMuni.addItem(query1.value(0))
        except Exception as error:
            print('Error en la selección de municipio', error)

    def modifCli(modcliente):
        try:
            print(modcliente)
            query = QtSql.QSqlQuery()
            query.prepare('update clientes set alta = :alta, apellidos = :apellidos, '
                          'nombre = :nombre, direccion = :direccion, provincia = :provincia, '
                          'municipio = :municipio, sexo = :sexo, pago = :pago, envio = :envio '
                          'where dni = :dni')
            query.bindValue(':dni', str(modcliente[0]))
            query.bindValue(':alta', str(modcliente[1]))
            query.bindValue(':apellidos', str(modcliente[2]))
            query.bindValue(':nombre', str(modcliente[3]))
            query.bindValue(':direccion', str(modcliente[4]))
            query.bindValue(':provincia', str(modcliente[5]))
            query.bindValue(':municipio', str(modcliente[6]))
            query.bindValue(':sexo', str(modcliente[7]))
            query.bindValue(':pago', str(modcliente[8]))
            query.bindValue(':envio', str(modcliente[9]))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Datos modificados de cliente')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Error en la modificación de clientes', error)

    def exportExcel(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_dataExport.xls')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.dlgabrir.getSaveFileName(None, 'Exportar datos', var.copia, '.xls',
                                                                options=option)
            wb = xlwt.Workbook()
            # add_sheet is used to create sheet.
            sheet1 = wb.add_sheet('Hoja 1')

            # Cabeceras
            sheet1.write(0, 0, 'DNI')
            sheet1.write(0, 1, 'APELIDOS')
            sheet1.write(0, 2, 'NOME')
            sheet1.write(0, 3, 'DIRECCION')
            sheet1.write(0, 4, 'PROVINCIA')
            sheet1.write(0, 5, 'SEXO')
            f = 1
            query = QtSql.QSqlQuery()
            query.prepare('SELECT *  FROM clientes')
            if query.exec_():
                while query.next():
                    sheet1.write(f, 0, query.value(0))
                    sheet1.write(f, 1, query.value(2))
                    sheet1.write(f, 2, query.value(3))
                    sheet1.write(f, 3, query.value(4))
                    sheet1.write(f, 4, query.value(5))
                    sheet1.write(f, 5, query.value(7))
                    f += 1
            wb.save(directorio)

        except Exception as error:
            print('Error en conexion para exportar excel ', error)

    def altaProd(newProd):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                'insert into productos (nombre, precio)'
                'VALUES (:nombre, :precio)')
            #query.bindValue(':codigo', str(newProd[0]))
            query.bindValue(':nombre', str(newProd[0]))
            query.bindValue(':precio', str(newProd[1]))

            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Producto dado de Alta')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Problemas alta productos', error)

    def bajaProd(producto):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from productos where nombre = :nombre')
            query.bindValue(':nombre', str(producto))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Producto eliminado')
                msg.exec()

        except Exception as error:
            print('Error eliminar producto en conexión', error)

    # def cargarTabProd(self):
    #     try:
    #         index = 0
    #         query = QtSql.QSqlQuery()
    #         query.prepare("select codigo, nombre, precio from productos order by codigo")
    #         if query.exec_():
    #             while query.next():
    #                 codigo = str(query.value(0))
    #                 nombre = query.value(1)
    #                 precio = str(query.value(2))
    #                 var.ui.tabProd.setRowCount(index + 1)
    #                 var.ui.tabProd.setItem(index, 0, QtWidgets.QTableWidgetItem(codigo))
    #                 var.ui.tabProd.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
    #                 var.ui.tabProd.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))
    #                 index += 1
    #
    #     except Exception as error:
    #         print('Problemas en mostrar listado productos', error)

    def cargarTabProd(self):
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio from productos order by nombre')
            if query.exec_():
                while query.next():
                    codigo = str(query.value(0))
                    producto = str(query.value(1))
                    precio = str(query.value(2))
                    var.ui.tabProd.setRowCount(index + 1)  # creamos la fila y luego cargamos datos
                    var.ui.tabProd.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                    var.ui.tabProd.setItem(index, 1, QtWidgets.QTableWidgetItem(producto))
                    var.ui.tabProd.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))
                    #from PyQt5.uic.properties import QtCore
                    var.ui.tabProd.item(index, 2).setTextAlignment(QtCore.Qt.AlignRight)
                    var.ui.tabProd.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    index += 1
        except Exception as error:
            print('Problemas mostrar tabla productos', error)

    # def modifProd(modprod):
    #     try:
    #         print(modprod)
    #         query = QtSql.QSqlQuery()
    #         query.prepare('update productos set codigo = :codigo, nombre = :nombre, precio = :precio '
    #                       'where codigo = :codigo')
    #         query.bindValue(':codigo', str(modprod[0]))
    #         query.bindValue(':nombre', str(modprod[1]))
    #         query.bindValue(':precio', str(modprod[2]))
    #
    #         if query.exec_():
    #             msg = QtWidgets.QMessageBox()
    #             msg.setWindowTitle('Aviso')
    #             msg.setIcon(QtWidgets.QMessageBox.Information)
    #             msg.setText('Datos modificados de producto')
    #             msg.exec()
    #         else:
    #             msg = QtWidgets.QMessageBox()
    #             msg.setWindowTitle('Aviso')
    #             msg.setIcon(QtWidgets.QMessageBox.Warning)
    #             msg.setText(query.lastError().text())
    #             msg.exec()
    #
    #     except Exception as error:
    #         print('Error en la modificación de productos', error)

    def modifProd(modpro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('update productos set nombre = :producto, precio = :precio where codigo = :cod')
            query.bindValue(':cod', int(modpro[0]))
            query.bindValue(':producto', str(modpro[1]))
            modpro[2] = modpro[2].replace('€', '')
            modpro[2] = modpro[2].replace(',', '.')
            modpro[2] = float(modpro[2])
            modpro[2] = round(modpro[2], 2)
            modpro[2] = str(modpro[2])
            #modpro[2] = locale.currency(float(modpro[2]))
            query.bindValue(':precio', str(modpro[2]))

            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Datos modificados de Producto')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('Error modificar producto en conexion: ', error)

    def buscarProducto(prod):
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio from productos '
                          'where nombre = :nombre')
            query.bindValue(':nombre', prod)
            if query.exec_():
                query.next()
                codigo = str(query.value(0))
                nombre = str(query.value(1))
                precio = str(query.value(2))
                var.ui.tabProd.setRowCount(index + 1)
                var.ui.tabProd.setItem(index, 0, QtWidgets.QTableWidgetItem(codigo))
                var.ui.tabProd.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.tabProd.setItem(index, 2, QtWidgets.QTableWidgetItem(precio))
            else:
                print('a')

            # prod = [codigo, nombre, precio]
            # row = 0
            # column = 0
            # var.ui.tabProd.insertRow(row)
            # for campo in prod:
            #     cell = QtWidgets.QTableWidgetItem(str(campo))
            #     var.ui.tabProd.setItem(row, column, cell)
            #     column += 1
        except Exception as error:
            print('Error en la búsqueda de un producto', error)

    '''
    Gestión facturas
    '''
    def buscaCliFac(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare('select apellidos, nombre from clientes where dni = :dni')
            query.bindValue(':dni', str(dni) )
            if query.exec_():
                while query.next():
                    registro.append(query.value(0))
                    registro.append(query.value(1))
                print(registro)
                return registro

        except Exception as error:
            print('Error en conexión buscar cliente', error)

    def altaFac(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into facturas (dni, fechafac) values (:dni, :fecha)')
            query.bindValue(':dni', str(registro[0]))
            query.bindValue(':fecha', str(registro[1]))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Factura dada de alta')
                msg.exec()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()

        except Exception as error:
            print('Error en conexión altaFac', error)

    # def cargaTabFacturas(self):
    #     try:
    #         index = 0
    #         query = QtSql.QSqlQuery()
    #         query.prepare('select codigo, fechafac from facturas order by fechafac desc')
    #         if query.exec_():
    #             while query.next():
    #                 codigo = str(query.value(0))
    #                 fechafac = str(query.value(1))
    #                 var.ui.tabFacturas.setRowCount(index + 1)
    #                 var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(codigo))
    #                 var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(fechafac))
    #                 index += 1
    #
    #     except Exception as error:
    #         print('Error en cargar la tabla de facturas', error)

    def cargaTabFacturas(self):
        try:
            index = 0
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, fechafac from facturas order by date(fechafac) desc ')
            if query.exec_():
                while query.next():
                    codigo = query.value(0)
                    fechafac = query.value(1)
                    var.btnfacdel = QtWidgets.QPushButton()
                    icopapelera = QtGui.QPixmap("img/bin.png")
                    var.btnfacdel.setFixedSize(24, 24)
                    var.btnfacdel.setIcon(QtGui.QIcon(icopapelera))
                    var.ui.tabFacturas.setRowCount(index + 1)  # creamos la fila y luego cargamos datos
                    var.ui.tabFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                    var.ui.tabFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(fechafac))
                    cell_widget = QtWidgets.QWidget()
                    lay_out = QtWidgets.QHBoxLayout(cell_widget)
                    lay_out.setContentsMargins(0, 0, 0, 0)
                    lay_out.addWidget(var.btnfacdel)
                    var.btnfacdel.clicked.connect(Conexion.bajaFac)
                    #lay_out.setAlignment(QtCore.Qt.AlignVCenter)
                    var.ui.tabFacturas.setCellWidget(index, 2, cell_widget)
                    var.ui.tabFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                    var.ui.tabFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignCenter)
                    index = index + 1

        except Exception as error:
            print('Error en carga listado facturas ', error)

    def buscaDNIFac(numFac):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select dni from facturas where codigo = :numFac')
            query.bindValue(':numFac', int(numFac))
            if query.exec_():
                while query.next():
                    dni = query.value(0)
            return dni

        except Exception as error:
            print('Error al buscar cliente de una factura', error)

    def buscaCodFac(self):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select codigo from facturas order by codigo desc limit 1')
            if query.exec_():
                while query.next():
                    codfac = query.value(0)
            return codfac

        except Exception as error:
            print('Error al buscar código de una factura', error)

    def bajaFac(self):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('delete from facturas where codigo = :codigo')
            query.bindValue(':codigo', str(var.ui.lblNumFactura.text()))
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Factura eliminada')
                msg.exec()
            Conexion.cargaTabFacturas(self)

        except Exception as error:
            print('Error al dar de baja una factura ', error)

    def cargarCmbProducto(self):
        try:
            var.cmbproducto.clear()
            query = QtSql.QSqlQuery()
            var.cmbproducto.addItem('') #primera línea en blanco
            query.prepare('select nombre from productos order by nombre')
            if query.exec_():
                while query.next():
                    var.cmbproducto.addItem(query.value(0))

        except Exception as error:
            print('Error al cargar un producto en la ComboBox ', error)

    def obtenerPrecio(articulo):
        try:
            dato = []
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, precio from productos where nombre = :nombre')
            query.bindValue(':nombre', str(articulo))
            if query.exec_():
                while query.next():
                    dato.append(int(query.value(0)))
                    dato.append(query.value(1))
            return dato

        except Exception as error:
            print('Error al cargar código precio en conexión ', error)

    def cargarVenta(venta):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into ventas (codfac, codprod, precio, cantidad) '
                          'values (:codfac, :codprod, :precio, :cantidad)')
            query.bindValue(':codfac', venta[0])
            query.bindValue(':codprod', venta[1])
            query.bindValue(':precio', venta[2])
            query.bindValue(':cantidad', venta[3])
            if query.exec_():
                var.ui.lblVenta.setText("Venta realizada")
                var.ui.lblVenta.setStyleSheet('QLabel {color: green;}')
            else:
                var.ui.lblVenta.setText("Error en venta")
                var.ui.lblVenta.setStyleSheet('QLabel {color: red;}')

        except Exception as error:
            print('Error al cargar venta ', error)







