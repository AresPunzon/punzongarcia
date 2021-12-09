import conexion
from ventana import *
import var
import locale
locale.setlocale( locale.LC_ALL, '' )


class Productos():
    # def guardaProd(self):
    #     try:
    #         newProd = []
    #         producto = [var.ui.txtProd, var.ui.txtPrecio]
    #         #tabProd = []
    #         #prod = [var.ui.txtProd, var.ui.txtPrecio]
    #         for i in producto:
    #             newProd.append(i.text())
    #         #for i in prod:
    #         #    tabProd.append(i.text())
    #         #row = 0
    #         #column = 0
    #         #var.ui.tabProd.insertRow(row)
    #         # for campo in tabProd:
    #         #     cell = QtWidgets.QTableWidgetItem(str(campo))
    #         #     var.ui.tabProd.setItem(row, column, cell)
    #         #     column += 1
    #         conexion.Conexion.altaProd(newProd)
    #         conexion.Conexion.cargarTabProd(self)
    #     except Exception as error:
    #         print('Error al guardar producto ', error)

    def guardaProd(self):
        try:
            registro = []
            producto = var.ui.txtProducto.text()
            producto = producto.title()
            registro.append(producto)
            precio = var.ui.txtPrecio.text()
            precio = precio.replace(',', '.')  # necesita estar con punto como en américa
            precio = locale.currency(float(precio))
            registro.append(precio)
            conexion.Conexion.altaProd(registro)
            conexion.Conexion.cargarTabPro(self)

        except Exception as error:
            print('Error en alta productos: ', error)

    def cargaProd(self):
        try:
            fila = var.ui.tabProd.selectedItems()
            datos = [var.ui.txtCod, var.ui.txtProd, var.ui.txtPrecio]

            if fila:
                row = [dato.text() for dato in fila]
            print(row)
            for i, dato in enumerate(datos):
                dato.setText(row[i])

        except Exception as error:
            print('Error al cargar datos de un producto ', error)

    def bajaProd(self):
        try:
            producto = var.ui.txtProd.text()
            conexion.Conexion.bajaProd(producto)
            conexion.Conexion.cargarTabProd(self)
        except Exception as error:
            print('Error al eliminar un producto ', error)

    def modifProd(self):
        try:
            modprod = []
            producto = [var.ui.txtCod, var.ui.txtProd, var.ui.txtPrecio]
            for i in producto:
                modprod.append(i.text())
            conexion.Conexion.modifProd(modprod)
            conexion.Conexion.cargarTabProd(self)

        except Exception as error:
            print('Error al modificar un producto ', error)

    def buscarProd(self):
        try:
            prod = var.ui.txtBuscar.text()
            conexion.Conexion.buscarProducto(prod)
        except Exception as error:
            print('Error al buscar un producto ', error)

















