# This Python file uses the following encoding: utf-8
import sys, random
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QDateEdit, QPushButton, QComboBox
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter, QFont
import conndb


class graph(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        #self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        #self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowTitle("Reporte en tiempo real")

        self.display_width = 640
        self.display_height = 480
        self.resize(self.display_width, self.display_height)

        self.emociones = ['Enojado','Disgustado','Miedo','Feliz','Neutral','Triste','Sorprendido']

        self.series = QBarSeries()

        self.series.setLabelsVisible(True)
        self.series.labelsPosition()

        #self.series.append(set0)
        #series.append(set1)

        self.chart = QChart()
        #self.chart.addSeries(self.series)
        self.chart.setTitle("Porcentaje de Emociones")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        # set font for chart title
        font = QFont()
        font.setPixelSize(20)
        self.chart.setTitleFont(font)

        self.axisX = QBarCategoryAxis()
        self.axisX.append(self.emociones)

        self.axisY = QValueAxis()
        #axisY.setRange(0, 100)
        self.axisY.setLabelsVisible(True)
        self.axisY.setMin(0)
        #self.axisY.setMax(max(porc_emocion))
        self.axisY.setLabelFormat("%.0f")
        self.axisY.setTitleText("Porcentaje")

        #self.chart.addAxis(self.axisX, Qt.AlignBottom)
        #self.chart.addAxis(self.axisY, Qt.AlignLeft)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)


        self.chartView = QChartView(self.chart)

        # create a horizontal and vertical box layout and add the widgets
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()


        self.combo = QComboBox()
        self.combo.addItem("Mostrar todos")
        self.combo.addItem("Filtar por fecha")
        self.combo.activated.connect(self.combo_click)

        # creating a QDateEdit object
        self.dateedit = QDateEdit(calendarPopup=True)
        self.dateedit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateedit.dateChanged.connect(self.dateedit_click)

        self.btn_actualizar = QPushButton('Actualizar')
        self.btn_actualizar.clicked.connect(self.load_emociones)

        hbox.addWidget(self.combo)
        hbox.addWidget(self.dateedit)
        hbox.addWidget(self.btn_actualizar)
        vbox.addLayout(hbox)
        vbox.addWidget(self.chartView)

        self.load_emociones()

        # set the vbox layout as the widgets layout
        self.setLayout(vbox)


    def load_emociones(self):
        self.series.clear()

        conn = conndb.conndb()
        strsql = "SELECT count(emocion) FROM emocion"
        result = conn.queryResult(strsql)
        total = int(result[0][0])
        print("Total registros", str(total))

        porc_emocion = []
        for emocion in self.emociones:
            strsql = ""
            filtro = self.combo.currentText()
            if filtro == "Filtar por fecha":
                qfecha = self.dateedit.date()
                fecha = '{0}-{1}-{2}'.format(qfecha.year(), qfecha.month(), qfecha.day())
                strsql = "SELECT count(emocion) FROM emocion WHERE emocion = '" + emocion + "' AND DATE(fecha) = '" + fecha + "'"
            else:
                strsql = "SELECT count(emocion) FROM emocion WHERE emocion = '" + emocion + "'"
            result = conn.queryResult(strsql)
            value = int(result[0][0]) / total * 100
            print(round(value, 2))
            porc_emocion.append(round(value, 2))

        print("porc emocion", porc_emocion)

        set0 = QBarSet('Emociones')
        #set1 = QBarSet('X1')

        set0.append(porc_emocion)
        #set1.append([random.randint(0, 10) for i in range(6)])
        self.series.append(set0)

        self.chart.addSeries(self.series)

        self.axisY.setMax(max(porc_emocion))

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

    def dateedit_click(self):
        filtro = self.combo.currentText()
        if filtro == "Filtar por fecha":
            self.load_emociones()

        # getting the date
        value = self.dateedit.date()
        value = '{0}-{1}-{2}'.format(value.year(), value.month(), value.day())
        print(value)

    def combo_click(self):
        filtro = self.combo.currentText()
        if filtro == "Mostrar todos":
            self.load_emociones()




