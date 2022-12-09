# This Python file uses the following encoding: utf-8
#from PyQt5 import QtCore
from PyQt5 import QtWidgets, uic
import conndb

class user_management(QtWidgets.QWidget):

    def __init__(self):     # funcion que se ejecuta al iniciar la clase
        super(user_management, self).__init__()
        uic.loadUi("user_management.ui", self)
        self.setWindowTitle("Gestión de Usuarios")

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.pushButton.clicked.connect(self.loadData)
        self.pushButton_Guardar.clicked.connect(self.saveData)
        self.pushButton_Eliminar.clicked.connect(self.deletData)
        self.tableWidget.clicked.connect(self.getItem)
        self.loadData()


    def loadData(self):     # función para cargar los datos del uruario en la tabla
        conn = conndb.conndb()
        strsql = "SELECT * FROM usuario"
        result = conn.queryResult(strsql)
        row = 0
        self.tableWidget.setRowCount(len(result))
        for user in result:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(user[1]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(user[2]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(user[3]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(user[4])))
            row = row + 1

    def saveData(self):     # función para actualizar los datos del usuario seleccionado
        id = self.lineEdit_Id.text()
        username = self.lineEdit_Username.text()
        password = self.lineEdit_Pass.text()
        privilegio = self.comboBox_Privilegio.currentText()
        activo = int(self.checkBox_Activo.isChecked())
        strsql = "UPDATE usuario SET nombre='{}', pass='{}', privilegio='{}', activo='{}' WHERE id='{}'".format(
            username,
            password,
            privilegio,
            activo,
            id)

        conn = conndb.conndb()
        conn.queryExecute(strsql)
        self.loadData()


    def deletData(self):    # funcion para eliminar los datos del usuario seleccionado
        id = self.lineEdit_Id.text()
        strsql = "DELETE FROM usuario WHERE id='"+id+"'"
        conn = conndb.conndb()
        conn.queryExecute(strsql)
        self.loadData()


    def getItem(self):      # funcion para mostrar en las cajas de texto los datos del usuario seleccionado de la tabla
        row = self.tableWidget.currentRow()

        rowItemId = self.tableWidget.item(row, 0).text()
        rowItemUsername = self.tableWidget.item(row, 1).text()
        rowItemPass = self.tableWidget.item(row, 2).text()
        rowItemPriv = self.tableWidget.item(row, 3).text()
        rowItemActivo = self.tableWidget.item(row, 4).text()

        self.lineEdit_Id.setText(str(rowItemId))
        self.lineEdit_Username.setText(rowItemUsername)
        self.lineEdit_Pass.setText(rowItemPass)
        self.comboBox_Privilegio.setCurrentText(rowItemPriv)
        self.checkBox_Activo.setChecked(int(rowItemActivo))


