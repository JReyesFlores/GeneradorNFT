# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainGeneradorNFT.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# view 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

# logic
from PIL import Image, ImageDraw, ImageChops
import random

# Model
from typing import Tuple
import uuid

class FileNFTModel(): 
    ruta_fisica = 'D:\\ZEGEL\\2.DO_CICLO\\Estructura de Datos\\ProyectoFinal2\\views\\assets\\news_nft'
    ruta_logica = '../assets/news_nft/'
    def __init__(self, nombre_nft: str, tamanio_ancho: int, tamanio_alto: int, 
                espaciado_interno: int, nro_linea: int, color_fondo: Tuple) -> None:
        self.__Id = str(uuid.uuid4())
        self.__NombreNFT = nombre_nft
        self.__Tamanio_Ancho = tamanio_ancho
        self.__Tamanio_Alto = tamanio_alto
        self.__Espaciado_Interno = espaciado_interno
        self.__Nro_Lineas = nro_linea
        self.__Color_Fondo = color_fondo
        self.ruta_logica = f'{self.ruta_logica}{self.__NombreNFT}.png'
    
    def __str__(self) -> str:
        return f'Id: {self.getId()}, Nombre: {self.getNombreNFT()}'
    
    def getId(self) -> str:
        return self.__Id
    
    def getNombreNFT(self) -> str:
        return self.__NombreNFT
    
    def setNombreNFT(self, nombre_nft: str) -> None:
        self.__NombreNFT = nombre_nft
    
    def getTamanioAncho(self) -> int:
        return self.__Tamanio_Ancho

    def setTamanioAncho(self, tamanio_ancho: int) -> None:
        self.__Tamanio_Ancho = tamanio_ancho

    def getTamanioAlto(self) -> int:
        return self.__Tamanio_Alto

    def setTamanioAlto(self, tamanio_alto: int) -> None:
        self.__Tamanio_Alto = tamanio_alto

    def getEspaciadoInterno(self) -> int:
        return self.__Espaciado_Interno

    def setEspaciadoInterno(self, espaciado_interno: int) -> None:
        self.__Espaciado_Interno = espaciado_interno

    def getNroLineas(self) -> int:
        return self.__Nro_Lineas

    def setNroLineas(self, nro_lineas: int) -> None:
        self.__Nro_Lineas = nro_lineas

    def getColorFondo(self) -> Tuple:
        return self.__Color_Fondo

    def setColorFondo(self, color_fondo: Tuple) -> None:
        self.__Color_Fondo = color_fondo

class NFTLogic():
    # Función para generar un RGB aleatorio
    def __random_color(self):
        return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    # Creamos las escalas de colores desde el color inicial hasta el final
    def __interpolate(self, start_color, end_color, factor: float):
        recip = 1 - factor
        return (
                int(start_color[0] * recip + end_color[0] * factor), 
                int(start_color[1] * recip + end_color[1] * factor),
                int(start_color[2] * recip + end_color[2] * factor)
                )

    # Generamos la imagen artistica (NFT)
    def generate_art(self, newFileNFT: FileNFTModel):
        print('Generando Arte NFT!')

        # Parametrizando las imagenes generadas
        image_width_size_px = newFileNFT.getTamanioAncho()
        image_height_size_px = newFileNFT.getTamanioAlto()
        image_padding = newFileNFT.getEspaciadoInterno()
        image_background_color = newFileNFT.getColorFondo()
        thickness = 0

        # definiendo la dimensión de la imagen
        image = Image.new('RGB', (image_width_size_px, image_height_size_px), image_background_color)
        
        # creando las líneas
        draw = ImageDraw.Draw(image)
        # start_position = (0, 0)
        # end_position = (60, 60)

        # Generando los puntos
        points = []
        for _ in range(newFileNFT.getNroLineas()):
            random_point = (
                random.randint(image_padding, image_width_size_px - image_padding), 
                random.randint(image_padding, image_width_size_px - image_padding))
            points.append(random_point)

        min_x = min([p[0] for p in points])
        max_x = max([p[0] for p in points])
        min_y = min([p[1] for p in points])
        max_y = max([p[1] for p in points])
        # draw.rectangle((min_x, min_y, max_x, max_y), outline=(255, 0, 0))

        # Centrar la imagen
        delta_x = min_x - (image_width_size_px - max_x)
        delta_y = min_y - (image_height_size_px - max_y)
        for i, point in enumerate(points):
            points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

        # Definiendo el color
        start_color = self.__random_color()
        end_color = self.__random_color()

        # Dibujando los puntos
        n_points = len(points) - 1
        for i, point in enumerate(points):
            # Overlay canvas
            overlay_image = Image.new('RGB', (image_width_size_px, image_height_size_px), image_background_color)
            overlay_draw = ImageDraw.Draw(overlay_image)
            point1 = point
            
            if i == n_points:
                point2 = points[0]
            else:
                point2 = points[i + 1]
            
            line_position_xy = (point1 , point2)
            color_factor = i / n_points

            # Multicolores
            # line_color = __random_color()
            line_color = self.__interpolate(start_color, end_color, color_factor)
            thickness += 1
            # draw.line(line_position_xy, fill= line_color, width=thickness)
            overlay_draw.line(line_position_xy, fill= line_color, width=thickness)
            image = ImageChops.add(image, overlay_image)
        
        # Guardando el archivo
        image.save(f'{FileNFTModel.ruta_fisica}\\{newFileNFT.getNombreNFT()}.png')
        print('Arte creado!')
    
    # Generamos la imagen artistica (NFT)
    def generate_massive_art(self, cantidad: int):
        lista = []
        for i in range(cantidad):
            nft_Item = FileNFTModel(f'nftNro_{i+1}', 128, 128, 10, 10, (0, 0, 0))
            lista.append(nft_Item)
            self.generate_art(nft_Item)
        return lista

class Ui_MainGeneradorNFT(object):
    ListaNFTs = []

    def setupUi(self, MainGeneradorNFT):
        MainGeneradorNFT.setObjectName("MainGeneradorNFT")
        MainGeneradorNFT.resize(932, 710)
        self.centralwidget = QtWidgets.QWidget(MainGeneradorNFT)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1461, 711))
        self.label.setStyleSheet("background-image: url('../assets/images/background-image-nft.jpg')")
        self.label.setText("")
        self.label.setObjectName("label")
        self.grpDatos_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.grpDatos_2.setGeometry(QtCore.QRect(0, 190, 551, 511))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.grpDatos_2.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.grpDatos_2.setFont(font)
        self.grpDatos_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.grpDatos_2.setObjectName("grpDatos_2")
        self.tblNFT = QtWidgets.QTableWidget(self.grpDatos_2)
        self.tblNFT.setGeometry(QtCore.QRect(10, 20, 531, 481))
        self.tblNFT.setObjectName("tblNFT")
        self.tblNFT.setColumnCount(5)
        self.tblNFT.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblNFT.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblNFT.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblNFT.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblNFT.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblNFT.setHorizontalHeaderItem(4, item)
        self.grpDatos_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.grpDatos_3.setGeometry(QtCore.QRect(560, 190, 361, 511))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.grpDatos_3.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.grpDatos_3.setFont(font)
        self.grpDatos_3.setStyleSheet("")
        self.grpDatos_3.setAlignment(QtCore.Qt.AlignCenter)
        self.grpDatos_3.setObjectName("grpDatos_3")
        self.lblImage = QtWidgets.QLabel(self.grpDatos_3)
        self.lblImage.setGeometry(QtCore.QRect(10, 20, 341, 481))
        self.lblImage.setAlignment(QtCore.Qt.AlignCenter)
        self.lblImage.setText("")
        self.lblImage.setObjectName("lblImage")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 941, 191))
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.grpDatos = QtWidgets.QGroupBox(self.tab)
        self.grpDatos.setGeometry(QtCore.QRect(10, 0, 921, 161))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.grpDatos.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.grpDatos.setFont(font)
        self.grpDatos.setStyleSheet("color: rgb(0, 0, 0);")
        self.grpDatos.setAlignment(QtCore.Qt.AlignCenter)
        self.grpDatos.setObjectName("grpDatos")
        self.label_3 = QtWidgets.QLabel(self.grpDatos)
        self.label_3.setGeometry(QtCore.QRect(360, 30, 81, 16))
        self.label_3.setObjectName("label_3")
        self.label_5 = QtWidgets.QLabel(self.grpDatos)
        self.label_5.setGeometry(QtCore.QRect(20, 30, 151, 16))
        self.label_5.setObjectName("label_5")
        self.txtNombreNFT = QtWidgets.QLineEdit(self.grpDatos)
        self.txtNombreNFT.setGeometry(QtCore.QRect(20, 50, 331, 20))
        self.txtNombreNFT.setObjectName("txtNombreNFT")
        self.txtAncho = QtWidgets.QLineEdit(self.grpDatos)
        self.txtAncho.setGeometry(QtCore.QRect(360, 50, 81, 20))
        self.txtAncho.setObjectName("txtAncho")
        self.txtAlto = QtWidgets.QLineEdit(self.grpDatos)
        self.txtAlto.setGeometry(QtCore.QRect(450, 50, 81, 20))
        self.txtAlto.setObjectName("txtAlto")
        self.label_6 = QtWidgets.QLabel(self.grpDatos)
        self.label_6.setGeometry(QtCore.QRect(450, 30, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.grpDatos)
        self.label_7.setGeometry(QtCore.QRect(540, 30, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.txtEspaciadoInterno = QtWidgets.QLineEdit(self.grpDatos)
        self.txtEspaciadoInterno.setGeometry(QtCore.QRect(540, 50, 111, 20))
        self.txtEspaciadoInterno.setObjectName("txtEspaciadoInterno")
        self.label_8 = QtWidgets.QLabel(self.grpDatos)
        self.label_8.setGeometry(QtCore.QRect(660, 30, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.txtNumeroLineas = QtWidgets.QLineEdit(self.grpDatos)
        self.txtNumeroLineas.setGeometry(QtCore.QRect(660, 50, 111, 20))
        self.txtNumeroLineas.setObjectName("txtNumeroLineas")
        self.sldRed = QtWidgets.QSlider(self.grpDatos)
        self.sldRed.setGeometry(QtCore.QRect(20, 120, 160, 22))
        self.sldRed.setMaximum(255)
        self.sldRed.setOrientation(QtCore.Qt.Horizontal)
        self.sldRed.setObjectName("sldRed")
        self.label_9 = QtWidgets.QLabel(self.grpDatos)
        self.label_9.setGeometry(QtCore.QRect(20, 80, 151, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.grpDatos)
        self.label_10.setGeometry(QtCore.QRect(20, 100, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.grpDatos)
        self.label_11.setGeometry(QtCore.QRect(200, 100, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.sldGreen = QtWidgets.QSlider(self.grpDatos)
        self.sldGreen.setGeometry(QtCore.QRect(200, 120, 160, 22))
        self.sldGreen.setMaximum(255)
        self.sldGreen.setOrientation(QtCore.Qt.Horizontal)
        self.sldGreen.setObjectName("sldGreen")
        self.label_12 = QtWidgets.QLabel(self.grpDatos)
        self.label_12.setGeometry(QtCore.QRect(380, 100, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.sldBlue = QtWidgets.QSlider(self.grpDatos)
        self.sldBlue.setGeometry(QtCore.QRect(380, 120, 160, 22))
        self.sldBlue.setMaximum(255)
        self.sldBlue.setOrientation(QtCore.Qt.Horizontal)
        self.sldBlue.setObjectName("sldBlue")
        self.RegistrarNFT = QtWidgets.QPushButton(self.grpDatos)
        self.RegistrarNFT.setGeometry(QtCore.QRect(630, 120, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.RegistrarNFT.setFont(font)
        self.RegistrarNFT.setObjectName("RegistrarNFT")
        self.btnGenerarNFT = QtWidgets.QPushButton(self.grpDatos)
        self.btnGenerarNFT.setGeometry(QtCore.QRect(770, 120, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnGenerarNFT.setFont(font)
        self.btnGenerarNFT.setObjectName("btnGenerarNFT")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.txtCantidadNFTs = QtWidgets.QLineEdit(self.tab_2)
        self.txtCantidadNFTs.setGeometry(QtCore.QRect(20, 40, 101, 21))
        self.txtCantidadNFTs.setObjectName("txtCantidadNFTs")
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(20, 20, 151, 16))
        self.label_13.setObjectName("label_13")
        self.btnGenerarMasivo = QtWidgets.QPushButton(self.tab_2)
        self.btnGenerarMasivo.setGeometry(QtCore.QRect(130, 40, 131, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnGenerarMasivo.setFont(font)
        self.btnGenerarMasivo.setObjectName("btnGenerarMasivo")
        self.tabWidget.addTab(self.tab_2, "")
        MainGeneradorNFT.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainGeneradorNFT)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainGeneradorNFT)

    def retranslateUi(self, MainGeneradorNFT):
        _translate = QtCore.QCoreApplication.translate
        MainGeneradorNFT.setWindowTitle(_translate("MainGeneradorNFT", "MainWindow"))
        self.grpDatos_2.setTitle(_translate("MainGeneradorNFT", "Lista del NFTs"))
        item = self.tblNFT.horizontalHeaderItem(0)
        item.setText(_translate("MainGeneradorNFT", "Id"))
        item = self.tblNFT.horizontalHeaderItem(1)
        item.setText(_translate("MainGeneradorNFT", "Nombre"))
        item = self.tblNFT.horizontalHeaderItem(2)
        item.setText(_translate("MainGeneradorNFT", "Ancho"))
        item = self.tblNFT.horizontalHeaderItem(3)
        item.setText(_translate("MainGeneradorNFT", "Alto"))
        item = self.tblNFT.horizontalHeaderItem(4)
        item.setText(_translate("MainGeneradorNFT", "Imagen"))
        self.grpDatos_3.setTitle(_translate("MainGeneradorNFT", "NFT Generado"))
        self.grpDatos.setTitle(_translate("MainGeneradorNFT", "Datos del NFT"))
        self.label_3.setText(_translate("MainGeneradorNFT", "Ancho:"))
        self.label_5.setText(_translate("MainGeneradorNFT", "Nombre del NFT:"))
        self.label_6.setText(_translate("MainGeneradorNFT", "Alto:"))
        self.label_7.setText(_translate("MainGeneradorNFT", "Espaciado Interno:"))
        self.label_8.setText(_translate("MainGeneradorNFT", "Números de Líneas:"))
        self.label_9.setText(_translate("MainGeneradorNFT", "Color (RGB):"))
        self.label_10.setText(_translate("MainGeneradorNFT", "Rojo (Red)"))
        self.label_11.setText(_translate("MainGeneradorNFT", "Verde (Green)"))
        self.label_12.setText(_translate("MainGeneradorNFT", "Azul (Blue)"))
        self.RegistrarNFT.setText(_translate("MainGeneradorNFT", "Registrar"))
        self.btnGenerarNFT.setText(_translate("MainGeneradorNFT", "Generar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainGeneradorNFT", "Individual"))
        self.label_13.setText(_translate("MainGeneradorNFT", "Cantidad de NFT\'s:"))
        self.btnGenerarMasivo.setText(_translate("MainGeneradorNFT", "Generar y Registrar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainGeneradorNFT", "Masiva"))

        # Agregando los eventos
        self.btnGenerarMasivo.clicked.connect(self.generar_masiva)
        self.btnGenerarNFT.clicked.connect(self.generar_individual)
        self.RegistrarNFT.clicked.connect(self.registrar_nft)
        self.tblNFT.selectionModel().selectionChanged.connect(self.on_selectionChanged)

    def on_selectionChanged(self, selected, deselected):
        try:
            items = self.tblNFT.selectedItems()
            if len(items) == 0:
                return

            for ix in selected.indexes():
                # print(f'Selected Cell Location Row: {ix.row()}, Column: {ix.column()}')
                item_NFT = self.ListaNFTs[ix.row()]
                # print(f'{item_NFT.ruta_logica}')
                self.lblImage.setStyleSheet("background-image: url('" + item_NFT.ruta_logica + "'); background-repeat: no-repeat;")

        except Exception as ex:
            self.msgBoxDialog(f'{ex}', True)

    def ListarNFT(self):
        self.EliminandoRegistros()
        for item in self.ListaNFTs:
            strArchivo = f'{FileNFTModel.ruta_fisica}\\{item.getNombreNFT()}.png'
            rowPos = self.tblNFT.rowCount()
            self.tblNFT.insertRow(rowPos)
            self.tblNFT.setItem(rowPos, 0, QTableWidgetItem(item.getId()))
            self.tblNFT.setItem(rowPos, 1, QTableWidgetItem(item.getNombreNFT()))
            self.tblNFT.setItem(rowPos, 2, QTableWidgetItem(str(item.getTamanioAncho())))
            self.tblNFT.setItem(rowPos, 3, QTableWidgetItem(str(item.getTamanioAlto())))
            self.tblNFT.setItem(rowPos, 4, QTableWidgetItem(strArchivo))

    def EliminandoRegistros(self):
        #self.tblNFT.clear()
        fila = self.tblNFT.rowCount()
        while fila >=0:
            if fila > 0:
                self.tblNFT.removeRow(fila-1)
            fila = fila - 1
    
    def msgBoxDialog(self, mensaje: str, esError: bool):
        msgBox = QMessageBox()
        msgBox.setWindowTitle('ZEGEL IPAE - Estructura de datos')
        msgBox.setText(f'{mensaje}')
        if esError:
            msgBox.setIcon(QMessageBox.Critical)
        else:
            msgBox.setIcon(QMessageBox.Information)
        msgBox.exec_()
    
    def generar_masiva(self):
        try:
            if not self.validacion_masiva():
                return

            cantidad_nfts = int(self.txtCantidadNFTs.text().strip()) 
            nftInstancia = NFTLogic()
            lista = nftInstancia.generate_massive_art(cantidad_nfts)
            for item in lista:
                self.ListaNFTs.append(item)
            
            self.msgBoxDialog('Generación masiva de NFTs realizada éxitosamente.', False)
            self.ListarNFT()
            
        except Exception as ex:
            self.msgBoxDialog(f'{ex}', True)

    def validacion_masiva(self):
        try:
            if self.txtCantidadNFTs.text().strip() == '':
                self.msgBoxDialog('La cantida de NFTs es obligatoria para generarlas.', True)
                return False
            
            if int(self.txtCantidadNFTs.text().strip()) == 0:
                self.msgBoxDialog('La cantida de NFTs es obligatoria para generarlas.', True)
                return False

            return True
        except ValueError:
            self.msgBoxDialog(f'Formato inválido en la cantidad de NFTs ingresada.', True)
        except Exception as ex:
            self.msgBoxDialog(f'{ex}', True)

    def generar_individual(self):
        try:
            if not self.validacion_individual():
                return
            
            tupla_color = (self.sldRed.value(), self.sldGreen.value(), self.sldBlue.value())
            print(tupla_color)
            newNFT = FileNFTModel(self.txtNombreNFT.text().strip(), int(self.txtAncho.text().strip()), 
                                int(self.txtAlto.text().strip()), int(self.txtEspaciadoInterno.text().strip()), int(self.txtNumeroLineas.text().strip()), 
                                tupla_color)

            nftInstancia = NFTLogic()
            nftInstancia.generate_art(newNFT)
            self.lblImage.setStyleSheet("background-image: url('" + newNFT.ruta_logica + "'); background-repeat: no-repeat;")
            
        except Exception as ex:
            self.msgBoxDialog(f'{ex}', True)

    def registrar_nft(self):
        try:
            if not self.validacion_individual():
                return
            
            tupla_color = (self.sldRed.value(), self.sldGreen.value(), self.sldBlue.value())
            newNFT = FileNFTModel(self.txtNombreNFT.text().strip(), int(self.txtAncho.text().strip()), 
                                int(self.txtAlto.text().strip()), int(self.txtEspaciadoInterno.text().strip()), int(self.txtNumeroLineas.text().strip()), 
                                tupla_color)

            nftInstancia = NFTLogic()
            nftInstancia.generate_art(newNFT)
            self.ListaNFTs.append(newNFT)
            self.msgBoxDialog('Registro del NFT realizado éxitosamente.', False)
            self.limpiar_controles()
            self.ListarNFT()
            
        except Exception as ex:
            self.msgBoxDialog(f'{ex}', True)
    
    def limpiar_controles(self):
        self.txtNombreNFT.setText('')
        self.txtAncho.setText('')
        self.txtAlto.setText('')
        self.txtEspaciadoInterno.setText('')
        self.txtNumeroLineas.setText('')
        self.sldBlue.setValue(0)
        self.sldGreen.setValue(0)
        self.sldRed.setValue(0)
    
    def validacion_individual(self):
        try:
            if self.txtNombreNFT.text().strip() == '':
                self.msgBoxDialog('El nombre del NFT es obligatorio.', True)
                return False 
            
            if self.txtAncho.text().strip() == '':
                self.msgBoxDialog('El ancho del NFT es obligatorio.', True)
                return False

            if self.txtAlto.text().strip() == '':
                self.msgBoxDialog('El alto del NFT es obligatorio.', True)
                return False 

            if self.txtEspaciadoInterno.text().strip() == '':
                self.msgBoxDialog('El espaciado interno del NFT es obligatorio.', True)
                return False 

            if self.txtNumeroLineas.text().strip() == '':
                self.msgBoxDialog('El Número de líneas del NFT es obligatorio.', True)
                return False 

            return True
        except Exception as ex:
            self.msgBoxDialog(f'{ex}', True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainGeneradorNFT = QtWidgets.QMainWindow()
    ui = Ui_MainGeneradorNFT()
    ui.setupUi(MainGeneradorNFT)
    MainGeneradorNFT.show()
    sys.exit(app.exec_())
