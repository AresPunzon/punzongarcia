from PyQt5 import QtSql, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Conexion:
    def db_connect(filedb):
        try:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(filedb)
            if not db.open:
                QtWidgets.QMessageBox.critical(None,
                    "No se puede abrir la base de alta.\n Haz clic para continuar",
                            QtWidgets.QMessageBox.Cancel)
                return False
            else:
                print("conexión establecida")
                return True
        except Exception as error:
            print ('Problemas en la conexión', error)

    '''
    Módulos gestión DB clientes
    '''
    # def altaCli(newCli):
    #     try:
    #         query = QtSql.QSqlQuery()
    #         query.prepare('insert into clientes (dni, alta, apellidos, nombre, direccion, provincia, municipio, sexo, pagos)'
    #                       'VALUES (:dni, :alta, :apellidos, :nombre, :direccion,:provincia, :municipio, :sexo, :pagos)')
    #         query.bindValue(':dni', str(newCli[0]))
    #         query.bindValue(':alta', str(newCli[1]))
    #         query.bindValue(':apellidos', str(newCli[2]))
    #         query.bindValue(':nombre', str(newCli[3]))
    #         query.bindValue(':direccion', str(newCli[4]))
    #         query.bindValue(':provincia', str(newCli[5]))
    #         query.bindValue(':municipio', str(newCli[6]))
    #         query.bindValue(':sexo', str(newCli[7]))
    #         query.bindValue(':pagos', str(newCli[8]))
    #
    #         if query.exec_:
    #             print(newCli)
    #             msgBox = QMessageBox()
    #             msgBox.setIcon(QtWidgets.QMessageBox.information)
    #             msgBox.setMinimumSize(1024, 1024)  # no hace nada
    #             msgBox.setWindowTitle('Alta en la BD')
    #             msgBox.setText("Cliente guardado en la BD")
    #             msgBox.exec()
    #         else:
    #             print('Error al guardar en la BD', query.lastError().text())
    #
    #     except Exception as error:
    #         print ('Problemas alta clientes', error)
    def altaCli(newCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('insert into clientes (dni, alta, apellidos, nombre, direccion, provincia, municipio,'
                          'sexo, pagos) VALUES (:dni, :alta, :apellidos, :nombre, :direccion, :provincia, :municipio,'
                          ':sexo, :pagos)')

            query.bindValue(':dni', str(newCli[0]))
            query.bindValue(':alta', str(newCli[1]))
            query.bindValue(':apellidos', str(newCli[2]))
            query.bindValue(':nombre', str(newCli[3]))
            query.bindValue(':direccion', str(newCli[4]))
            query.bindValue(':provincia', str(newCli[5]))
            query.bindValue(':municipio', str(newCli[6]))
            query.bindValue(':sexo', str(newCli[7]))
            query.bindValue(':pagos', str(newCli[8]))
            print(newCli)
            if query.exec_():
                print('alta cliente')
            else:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle('Aviso')
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(query.lastError().text())
                msg.exec()
        except Exception as error:
            print('Problemas en altaCliente', error)