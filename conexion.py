from PyQt5 import QtSql, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import var


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
            print ('Problemas en la conexión', error)

    '''
    Módulos gestión DB clientes
    '''
    def altaCli(newCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into clientes (dni, alta, apellidos, nombre, direccion, provincia, municipio, sexo, pago)'
                          'VALUES (:dni, :alta, :apellidos, :nombre, :direccion,:provincia, :municipio, :sexo, :pago)')
            query.bindValue(':dni', str(newCli[0]))
            query.bindValue(':alta', str(newCli[1]))
            query.bindValue(':apellidos', str(newCli[2]))
            query.bindValue(':nombre', str(newCli[3]))
            query.bindValue(':direccion', str(newCli[4]))
            query.bindValue(':provincia', str(newCli[5]))
            query.bindValue(':municipio', str(newCli[6]))
            query.bindValue(':sexo', str(newCli[7]))
            query.bindValue(':pago', str(newCli[8]))

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
            print ('Problemas alta clientes', error)

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
                    var.ui.tabCliente.setRowCount(index+1)    #creamos la fila y cargamos datos
                    var.ui.tabCliente.setItem(index,0,QtWidgets.QTableWidgetItem(dni))
                    var.ui.tabCliente.setItem(index,1,QtWidgets.QTableWidgetItem(apellidos))
                    var.ui.tabCliente.setItem(index,2,QtWidgets.QTableWidgetItem(nombre))
                    var.ui.tabCliente.setItem(index,3,QtWidgets.QTableWidgetItem(alta))
                    var.ui.tabCliente.setItem(index,4,QtWidgets.QTableWidgetItem(pago))
                    index += 1

        except Exception as error:
            print('Problemas en mostrar listado clientes', error)

    def oneClie(dni):
        try:
            record = []
            query = QtSql.QSqlQuery()
            query.prepare('select direccion, provincia, municipio, sexo from clientes '
                          'where dni = :dni')
            query.bindValue(':dni', dni)
            if query.exec_():
                while query.next():
                    for i in range(4):
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
                          'nombre = :nombre, direccion = : direccion, provincia = :provincia, '
                          'municipio = :municipio, sexo = :sexo, pago = :pago '
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
            if query.exec_():
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Datos modificados de cliente')
                msg.exec()
            else:
                print('a')

        except Exception as error:
            print('Error en la modificación de clientes', error)







