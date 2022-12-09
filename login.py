# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import conndb

class login(QtWidgets.QDialog):
    def __init__(self):
        super(login, self).__init__()
        uic.loadUi("login.ui", self)
        self.setWindowTitle("Iniciar Sesión")
        self.pushButton_Login.clicked.connect(self.login)

    def login(self):
        username = self.lineEdit_Username.text()
        password = self.lineEdit_Pass.text()
        strsql = "SELECT `nombre`, `pass` FROM usuario WHERE nombre='"+username+"' AND pass='"+password+"' AND activo=1"
        conn = conndb.conndb()
        result = conn.queryResult(strsql)
        if len(result)==1:
            self.result = result
            self.close()
        else:
            QMessageBox.about(self, "Iniciar Sesión", "Acceso Denegado")

