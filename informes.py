from reportlab.pdfgen import canvas
import os, var

class Informes:

    def ListadoCliente(self):
        try:
            var.cv = canvas.Canvas('informes/listadoclientes.pdf')
            Informes.cabecera(self)
            # var.cv.setFont('Helvetica-Bold', 16)
            # var.cv.drawString(100, 750, 'Listado clientes')
            # var.cv.line(30,400,500,400) #línea
            # var.cv.circle(150,100,100, stroke= 1, fill= 1)
            # text = "Este es un ejemplo de párrafo en el informe \nque estoy creando"
            # var.cv.setFont("Courier-Oblique", 10)
            # var.cv.drawString(100, 300, text)
            rootPath = '.\\informes'
            var.cv.setFont('Helvetica-Bold', 8)
            var.ui.setTitle("Listado clientes")
            var.ui.setAuthor("Departamento de administración")
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
            var.cv.line(40,800,500,800)
            var.cv.setFont('Helvetica-Bold', 14)
            var.cv.drawString(50,785, "Import-Export Vigo")
            var.cv.setFont('Helvetica', 10)
            var.cv.drawString(50,770, "CIF 00000000")
            var.cv.drawString(50, 755, "Dirección Avenida Galicia 101")
            var.cv.drawString(50, 740, "Vigo - 123 - Spain")
            var.cv.drawString(50, 725, "mail: correo@mail.com")
            var.cv.drawImage(logo, 425,725)
            var.cv.line(40,710,500,710)

        except Exception as error:
            print('Error al hacer la cabecera del informe ', error)
