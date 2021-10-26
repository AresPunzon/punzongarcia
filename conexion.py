from PyQt5 import QtSql, QtWidgets

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
    def altaCli(newCli):
        try:
            pass
        except Exception as error:
            print ('Problemas alta clientes', error)