# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtWidgets, uic, QtCore
#from PyQt5.QtWidgets import QMessageBox

import user_management as usr_mgt
import login
import live_cam
import graph
#import cliente

class main(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Identificación de Antecedentes")
        self.showMaximized()

        #self.mdiArea.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.mdiArea.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.mdiArea.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.logout()
        self.actionLogin.triggered.connect(self.login)
        self.actionLogout.triggered.connect(self.logout)
        self.actionIniciar_Camara.triggered.connect(self.l_cam)
        self.actionEstadisticas_Emociones.triggered.connect(self.graph_show)
        self.actionGestion_de_Usuarios.triggered.connect(self.user_mgt)
        #self.actionClientes.triggered.connect(self.clientes_show)

    """
    def clientes_show(self):
        self.clientes_frm = cliente.cliente()
        #self.mdiArea.addSubWindow(self.usr_mgt_w)
        self.clientes_frm.show()
    """
    def login(self):
        self.lg = login.login()
        self.lg.exec()
        result = self.lg.result
        try:
            if len(result)==1:
                self.menuAdmin.setEnabled(True)
                self.menuCamara.setEnabled(True)
                #self.menuClientes.setEnabled(True)
                self.menuReportes.setEnabled(True)
        except:
            pass

    def logout(self):
        self.menuAdmin.setEnabled(False)
        self.menuCamara.setEnabled(False)
        #self.menuClientes.setEnabled(False)
        self.menuReportes.setEnabled(False)


    def user_mgt(self):
        self.usr_mgt_w = usr_mgt.user_management()
        #self.mdiArea.addSubWindow(self.usr_mgt_w)
        self.usr_mgt_w.show()

    def l_cam(self):
        for w in self.mdiArea.subWindowList():
            if str(w.widget().objectName()) == "cam":
                return

        self.live_cam = live_cam.live_cam()
        self.live_cam.setObjectName("cam")

        #mdi = self.mdiArea.addSubWindow(self.live_cam, QtCore.Qt.FramelessWindowHint)
        mdi = self.mdiArea.addSubWindow(self.live_cam)
        self.live_cam.setGeometry(0, 0, 660, 500)
        self.live_cam.show()
        mdi.resize(640, 480)



    def graph_show(self):
        for w in self.mdiArea.subWindowList():
            if str(w.widget().objectName()) == "graph":
                return

        self.graph = graph.graph()
        self.graph.setObjectName("graph")

        mdi = self.mdiArea.addSubWindow(self.graph)
        self.graph.setGeometry(0, 0, 660, 500)
        self.graph.show()
        mdi.resize(640, 480)


app = QtWidgets.QApplication(sys.argv)

screen = app.primaryScreen()
#print('Screen: %s' % screen.name())
#size = screen.size()
#print('Size: %d x %d' % (size.width(), size.height()))
rect = screen.availableGeometry()
#print('Available: %d x %d' % (rect.width(), rect.height()))

widget = main()
widget.mdiArea.resize(rect.width(), rect.height() - 70)
widget.show()
app.exec()
