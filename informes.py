from PyQt5 import QtSql
from reportlab.pdfgen import canvas
import os, var
from datetime import datetime

class Informes:

    def ListadoCliente(self):
        try:
            var.cv = canvas.Canvas('informes/listadoclientes.pdf')
            Informes.cabecera(self)

            #var.cv.setFont('Helvetica-Bold', 16)
            # var.cv.drawString(100, 750, 'Listado clientes')
            # var.cv.line(30,400,500,400) #línea
            # var.cv.circle(150,100,100, stroke= 1, fill= 1)
            # text = "Este es un ejemplo de párrafo en el informe \nque estoy creando"
            # var.cv.setFont("Courier-Oblique", 10)
            # var.cv.drawString(100, 300, text)

            rootPath = '.\\informes'
            var.cv.setFont('Helvetica-Bold', size = 10)
            textoTitulo = 'Listado Clientes'
            Informes.pie(textoTitulo)
            var.cv.drawString(255, 690, textoTitulo)
            var.cv.line(40, 685, 530, 685)
            items = ['DNI', 'Nombre', 'Formas de pago']
            var.cv.drawString(70, 675, items[0])
            var.cv.drawString(210, 675, items[1])
            var.cv.drawString(370, 675, items[2])
            var.cv.line(40, 670, 530, 670)
            query = QtSql.QSqlQuery()
            query.prepare('select dni, apellidos, nombre, pago from clientes order by apellidos, nombre')
            var.cv.setFont('Helvetica', size = 8)
            if query.exec_():
                i = 50
                j = 655
                while query.next():
                    if j <= 80:
                        var.cv.drawString(440, 30, 'Página siguiente...')
                        var.cv.showPage()
                        Informes.cabecera(self)
                        Informes.pie(textoTitulo)
                        var.cv.drawString(255, 690, textoTitulo)
                        var.cv.line(40, 685, 530, 685)
                        items = ['DNI', 'Nombre', 'Formas de pago']
                        var.cv.drawString(70, 675, items[0])
                        var.cv.drawString(210, 675, items[1])
                        var.cv.drawString(370, 675, items[2])
                        var.cv.line(40, 670, 530, 670)
                        i = 50
                        j = 655

                    var.cv.setFont('Helvetica', size= 8)
                    var.cv.drawString(i, j, str(query.value(0)))
                    var.cv.drawString(i+140, j, str(query.value(1) + ', ' + query.value(2)))
                    var.cv.drawString(i+310, j, str(query.value(3)))
                    j = j - 20

            #var.ui.setTitle("Listado clientes")
            #var.ui.setAuthor("Departamento de administración")

            var.cv.save()
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont +1

        except Exception as error:
            print('Error al hacer el informe ', error)

    def cabecera(self):
        try:
            logo = '.\\img\linux.png'
            var.cv.line(40,800,530,800)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50,785, "Import-Export Vigo")
            var.cv.setFont('Helvetica', 10)
            var.cv.drawString(50,770, "CIF 00000000")
            var.cv.drawString(50, 755, "Dirección Avenida Galicia 101")
            var.cv.drawString(50, 740, "Vigo - 123 - Spain")
            var.cv.drawString(50, 725, "mail: correo@mail.com")
            var.cv.drawImage(logo, 425,725)
            var.cv.line(40,710,530,710)

        except Exception as error:
            print('Error al hacer la cabecera del informe ', error)

    def pie(texto):
        try:
            var.cv.line(50, 50, 530, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%dd.%mm.%yyyy %H.%M.%S')
            var.cv.setFont('Helvetica', size = 6)
            var.cv.drawString(70, 40, str(fecha))
            var.cv.drawString(255, 40, str(texto))
            var.cv.drawString(500, 40, str('Página %s' %var.cv.getPageNumber()))


        except Exception as error:
            print('Error al creación pie del informe ', error)























