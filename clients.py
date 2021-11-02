from PyQt5.QtWidgets import QMessageBox

import conexion
from ventana import *
import var


class Clientes():
    def validarDNI():
        try:
            escribir = False  # para guardarCli
            dni = var.ui.txtdni.text()  # convertir letra en mayuscula
            var.ui.txtdni.setText(dni.upper())
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'  # letras dni
            dig_ext = 'XYZ'  # digito extranjero
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = '1234567890'
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    var.ui.lblvalidodni.setStyleSheet('QLabel {color:green;}')
                    var.ui.lblvalidodni.setText('V')
                    escribir = True
                else:
                    var.ui.lblvalidodni.setStyleSheet('QLabel {color:red;}')
                    var.ui.lblvalidodni.setText('X')
                    var.ui.txtdni.setStyleSheet('background-color: rgb(255,0,0)')
                    escribir = False
            else:
                var.ui.lblvalidodni.setStyleSheet('QLabel {color:red;}')
                var.ui.lblvalidodni.setText('X')
                var.ui.txtdni.setStyleSheet('background-color: rgb(255,0,0)')
                escribir = False

            return escribir
        except Exception as error:
            print('Error en modulo valor dni. ', error)

    # def setSexo(self):
    #     try:
    #         if var.ui.rbtHome.isChecked():
    #             print('Marcado masculino')
    #         elif var.ui.rbtMujer.isChecked():
    #             print('Marcado femenino')
    #     except Exception as error:
    #         print('Error al seleccionar sexo ', error)
    #
    # def setPago(self):
    #     try:
    #         if var.ui.chkEfectivo.isChecked():
    #             print('Has seleccionado efectivo')
    #         if var.ui.chkTarjeta.isChecked():
    #             print('Has seleccionado tarjeta')
    #         if var.ui.chkTrans.isChecked():
    #             print('Has seleccionado tranferencia')
    #         if var.ui.chkCargoCuenta.isChecked():
    #             print('Has seleccionado cargo a cuenta')
    #     except Exception as error:
    #         print('Error al seleccionar forma de pago ', error)

    def cargaProv(self):
        try:
            var.ui.cmbProv.clear()
            prov = ["", "A Coruña", "Lugo", "Ourense", "Pontevedra"]
            for i in prov:
                var.ui.cmbProv.addItem(i)
        except Exception as error:
            print('Error en el módulo cargar provincia, ', error)

    # def selProv(prov):
    #     try:
    #         print('Has seleccionado la provincia de ', prov)
    #     except Exception as error:
    #         print('Error en el módulo seleccionar provincia, ', error)

    def cargaMuni(self):
        try:
            var.ui.cmbMuni.clear()
            muni = ["", "a"]
            for i in muni:
                var.ui.cmbMuni.addItem(i)
        except Exception as error:
            print('Error en el módulo cargar municipio, ', error)

    # def selMuni(muni):
    #     try:
    #         print('Has seleccionado el municipio de ', muni)
    #     except Exception as error:
    #         print('Error en el módulo seleccionar municipio, ', error)

    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.txtAlta.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as error:
            print('Error al cargar fecha, ', error)

    def mayuscNome():
        try:
            nome = var.ui.txtNome.text()
            var.ui.txtNome.setText(nome.capitalize())  # capitalize pone en mayus la primera letra de la primera palabra
        except Exception as error:
            print('Error al escribir el nombre ', error)

    def mayuscApe():
        try:
            ape = var.ui.txtApe.text()
            var.ui.txtApe.setText(ape.title())  # title pone en mayusc la primera de cada palabra
        except Exception as error:
            print('Error al escribir los apellidos ', error)

    def mayuscDir():
        try:
            dir = var.ui.txtDir.text()
            var.ui.txtDir.setText(dir.title())
        except Exception as error:
            print('Error al escribir la dirección ', error)

    def guardaCli(self):
        try:
            if Clientes.validarDNI() == True:
                # Preparamos el registro
                newCli = []
                cliente = [var.ui.txtdni, var.ui.txtAlta, var.ui.txtApe, var.ui.txtNome, var.ui.txtDir]  # para la BD
                tabCli = []  # para la tableView
                client = [var.ui.txtdni, var.ui.txtApe, var.ui.txtNome, var.ui.txtAlta]
                # código para cargar la tabla
                for i in cliente:
                    newCli.append(i.text())
                for i in client:
                    tabCli.append(i.text())
                newCli.append(var.ui.cmbProv.currentText())
                newCli.append(var.ui.cmbMuni.currentText())
                if var.ui.rbtHome.isChecked:
                    newCli.append("Hombre")
                elif var.ui.rbtMujer.isChecked:
                    newCli.append("Mujer")
                row = 0
                column = 0
                pagos = []
                if var.ui.chkCargoCuenta.isChecked():
                    pagos.append('Cargo cuenta')
                if var.ui.chkTrans.isChecked():
                    pagos.append('Transferencia')
                if var.ui.chkEfectivo.isChecked():
                    pagos.append('Efectivo')
                if var.ui.chkTarjeta.isChecked():
                    pagos.append('Tarjeta')
                pagos = set(pagos)  # evita duplicados
                tabCli.append(', '.join(pagos))
                newCli.append(', '.join(pagos))
                # cargamos la tabla
                row = 0
                column = 0
                var.ui.tabCliente.insertRow(row)
                for campo in tabCli:
                    cell = QtWidgets.QTableWidgetItem(str(campo))
                    var.ui.tabCliente.setItem(row, column, cell)
                    column += 1
                conexion.Conexion.altaCli(newCli)

            else:
                # print('DNI no válido')
                msgBox = QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setMinimumSize(1024, 1024)  # no hace nada
                msgBox.setWindowTitle('Aviso DNI')
                msgBox.setText("DNI inválido")
                msgBox.exec()

            # código para cargar la DB
        except Exception as error:
            print('Error al guardar clientes ', error)

    def limpiarForm(self):
        try:
            var.ui.txtdni.setText("")
            var.ui.txtApe.setText("")
            var.ui.txtNome.setText("")
            var.ui.txtDir.setText("")
            var.ui.txtAlta.setText("")
            var.ui.cmbProv.clear
            var.ui.cmbMuni.clear
            var.ui.chkTrans.setChecked(False)
            var.ui.chkCargoCuenta.setChecked(False)
            var.ui.chkTarjeta.setChecked(False)
            var.ui.chkEfectivo.setChecked(False)
            # Selecciona el "" que creamos cuando hicimos los comboBox
            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.cmbMuni.setCurrentIndex(0)
            # Primero quitar exclusividad y luego volver a ponerla
            var.ui.rbtGroupSex.setExclusive(False)
            var.ui.rbtHome.setChecked(False)
            var.ui.rbtMujer.setChecked(False)
            var.ui.rbtGroupSex.setExclusive(True)

        except Exception as error:
            print('Error al limpiar el formulario ', error)

    def cargaCli(self):
        try:
            fila = var.ui.tabCliente.selectedItems()
            datos = [var.ui.txtdni, var.ui.txtApe, var.ui.txtNome, var.ui.txtAlta]

            if fila:
                row = [dato.text() for dato in fila]
            print(row)
            for i, dato in enumerate(datos):    #cargamos los datos en las cajas de texto
                dato.setText(row[i])
            if 'Efectivo' in row[4]:
                var.ui.chkEfectivo.setChecked(True)
            if 'Tarjeta' in row[4]:
                var.ui.chkTarjeta.setChecked(True)
            if 'Transferencia' in row[4]:
                var.ui.chkTrans.setChecked(True)
            if 'Cargo' in row[4]:
                var.ui.chkCargoCuenta.setChecked(True)

            ''' Intentar pillar el resto de los datos '''
            query = QtSql.QSqlQuery()
            query.prepare("select direccion, provincia, municipio, sexo from clientes "
                          "where dni = :dni")
            query.bindValue (":dni", dni)
            print(dni)
            if query.exec_():


        except Exception as error:
            print('Error al cargar datos de un cliente ', error)
