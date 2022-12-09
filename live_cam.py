from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import conndb

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import cv2
import imutils
import time
import numpy as np


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # Variables para calcular FPS
        time_actualframe = 0
        time_prevframe = 0

        # Tipos de emociones del detector
        classes = ['Enojado','Disgustado','Miedo','Feliz','Neutral','Triste','Sorprendido']

        # Cargamos el  modelo de detección de rostros
        prototxtPath = r"face_detector\deploy.prototxt"
        weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
        faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

        # Carga el detector de clasificación de emociones
        emotionModel = load_model("model.h5")

        # Se crea la captura de video
        cam = cv2.VideoCapture(0)

        while self._run_flag:
            # Se toma un frame de la cámara y se redimensiona
            ret, frame = cam.read()
            frame = imutils.resize(frame, width=640)

            # Construye un blob de la imagen
            blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),(104.0, 177.0, 123.0))
            # Realiza las detecciones de rostros a partir de la imagen
            faceNet.setInput(blob)
            detections = faceNet.forward()
            # Listas para guardar rostros, ubicaciones y predicciones
            faces = []
            locs = []
            preds = []
            # Recorre cada una de las detecciones
            for i in range(0, detections.shape[2]):
                # Fija un umbral para determinar que la detección es confiable
                # Tomando la probabilidad asociada en la deteccion
                if detections[0, 0, i, 2] > 0.4:
                    # Toma el bounding box de la detección escalado
                    # de acuerdo a las dimensiones de la imagen
                    box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                    (Xi, Yi, Xf, Yf) = box.astype("int")
                    # Valida las dimensiones del bounding box
                    if Xi < 0: Xi = 0
                    if Yi < 0: Yi = 0
                    # Se extrae el rostro y se convierte BGR a GRAY
                    # Finalmente se escala a 224x244
                    face = frame[Yi:Yf, Xi:Xf]
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    face = cv2.resize(face, (48, 48))
                    face2 = img_to_array(face)
                    face2 = np.expand_dims(face2,axis=0)
                    # Se agrega los rostros y las localizaciones a las listas
                    faces.append(face2)
                    locs.append((Xi, Yi, Xf, Yf))

                    pred = emotionModel.predict(face2)
                    preds.append(pred[0])


            # Para cada hallazgo se dibuja en la imagen el bounding box y la clase
            for (box, pred) in zip(locs, preds):

                (Xi, Yi, Xf, Yf) = box
                (angry,disgust,fear,happy,neutral,sad,surprise) = pred

                label = ''
                # Se agrega la probabilidad en el label de la imagen
                label = "{}: {:.0f}%".format(classes[np.argmax(pred)], max(angry,disgust,fear,happy,neutral,sad,surprise) * 100)


                #print(classes[np.argmax(pred)])
                strsql = "INSERT INTO emocion (emocion) VALUES('{}')".format(classes[np.argmax(pred)])
                conn = conndb.conndb()
                try:
                    conn.queryExecute(strsql)
                    #print("Emoción registrada correctamente")
                except:
                    print("Error al registrar la emoción")


                cv2.rectangle(frame, (Xi, Yi-40), (Xf, Yi), (255,0,0), -1)
                cv2.putText(frame, label, (Xi+5, Yi-15),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                cv2.rectangle(frame, (Xi, Yi), (Xf, Yf), (255,0,0), 3)



            time_actualframe = time.time()
            if time_actualframe>time_prevframe:
                fps = 1/(time_actualframe-time_prevframe)
            time_prevframe = time_actualframe
            cv2.putText(frame, str(int(fps))+" FPS", (5, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)

            if ret:
                self.change_pixmap_signal.emit(frame)

        cam.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class live_cam(QWidget):
    def __init__(self):
        super().__init__()
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        #self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowTitle("Cámara - Detección de Sentimientos")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    
