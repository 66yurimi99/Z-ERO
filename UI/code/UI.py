import sys
import cv2
import requests
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtCore import *

# Start Window
class FirstWindow(QMainWindow):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):
        #apply Project name image to main UI
        title_load = QPixmap('./images/Z_ERO.png')
        title_img = QLabel(self)
        title_img.setPixmap(title_load)
        title_img.setGeometry(180, 100, title_load.width(), title_load.height())

        #Input Car Number to main UI
        self.input_CarNumber = QLineEdit(self)
        self.input_CarNumber.setText('차량 번호를 입력해주세요 (ENTER)')
        self.input_CarNumber.setStyleSheet("color: black; border: 3px solid black;")
        self.input_CarNumber.setAlignment(Qt.AlignCenter)
        self.input_CarNumber.setGeometry(450,500,300,50)
        self.input_CarNumber.mousePressEvent = self.clearText

        #apply Next button image to main UI
        next_btn = QPushButton(self)
        next_btn.setGeometry(680, 565, 70, 70)
        next_btn.setStyleSheet("border-image:url(./images/next.png)")
        next_btn.clicked.connect(self.showSecondWindow)


        #show main UI
        self.setGeometry(400, 200, 1200, 700)
        self.setStyleSheet("background : white;")
        self.inform_label = QLabel('오른쪽 이미지를\n    눌러주세요',self)
        self.inform_label.setGeometry(480,550,200,100)

        font = QFont()
        font.setPointSize(15)
        self.inform_label.setFont(font)
        self.setStyleSheet("background : white;")

        self.show()

    def sendCarNumber(self):

        #send Car Number to server
        CarNumber=self.input_CarNumber.text()
        QMessageBox.about(self,'차량 등록',f'★ [{CarNumber}] 등록 완료 ★')

        #Todo
        #DMS한테 차량번호 넘겨주기

        #send Car Number to server
        #CarNumber=self.input_CarNumber.text()
        #url=f'http://54.175.8.12/db.php?number={CarNumber}'
        #response = requests.get(url)
        #QMessageBox.about(self,'차량 등록',f'★ [{CarNumber}] 등록 완료 ★')

    def clearText(self, event):
            self.input_CarNumber.clear()
            self.input_CarNumber.selectAll()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.sendCarNumber()
            event.accept()

    def saveCarNumber(self):
        CarNumber=self.input_CarNumber.text()
        return CarNumber

    def showSecondWindow(self):
        second_window = SecondWindow(self)
        self.hide()
        second_window.show()

"""
-----------------------------------------------------------------------------------------------------------------------------
"""

#Second Window
class SecondWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.myCarNumber = parent.saveCarNumber()

        self.initUI()

    def initUI(self):
        # Set font and size for labels
        self.inform_Driver = QLabel('Driver',self)
        self.inform_Car = QLabel('Car',self)
        self.inform_Processing = QLabel('Processing',self)

        self.inform_Driver.move(150, 40)
        self.inform_Car.move(560, 40)
        self.inform_Processing.move(930, 40)

        self.background_label = QLabel(self)
        self.background_label.setGeometry(0,100,1200,450)
        self.background_label.setStyleSheet("background : black;")

        # set Driver video to main UI
        self.Driver_label = QLabel(self)
        self.Driver_label.setStyleSheet("background : black;")
        self.Driver_label.resize(300, 450)
        self.Driver_label.move(50, 100)

        # set Car video to main UI
        self.Car_label = QLabel(self)
        self.Car_label.setStyleSheet("background : black;")
        self.Car_label.resize(300, 450)
        self.Car_label.move(450, 100)

        # set Processing video to main UI
        self.Processing_label = QLabel(self)
        self.Processing_label.setStyleSheet("background : black;")
        self.Processing_label.resize(300, 450)
        self.Processing_label.move(850, 100)

        # show CarNumber to main UI
        self.textCar_label = QLabel('차량 번호',self)
        self.myCarNumber_label=QLabel(f'{self.myCarNumber}',self)
        self.textCar_label.move(130, 580)
        self.myCarNumber_label.move(125,630)

        # Set font for labels
        font = QFont()
        font.setPointSize(20)
        self.inform_Driver.setFont(font)
        self.inform_Car.setFont(font)
        self.inform_Processing.setFont(font)
        self.textCar_label.setFont(font)
        self.myCarNumber_label.setFont(font)

        # Set styles for labels
        self.inform_Driver.setStyleSheet("color: red;" "border-style: solid;")
        self.inform_Car.setStyleSheet("color: green;" "border-style: solid;")
        self.inform_Processing.setStyleSheet("color: blue;" "border-style: solid;")
        self.textCar_label.setStyleSheet("border-style: solid;")
        self.myCarNumber_label.setStyleSheet("border-style: solid;")

        # apply start button image to main UI
        self.start_image = QPixmap("./images/start.png")
        self.start_processed_image = self.start_image.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.start_btn = QPushButton(self)
        self.start_btn.setIcon(QIcon(self.start_processed_image))
        self.start_btn.setIconSize(self.start_processed_image.size())
        self.start_btn.move(400, 560)
        self.start_btn.clicked.connect(self.start_threads)

        #gif
        self.start_gif = QMovie("./images/start.gif")
        self.start_gif.setScaledSize(QSize(140, 140))
        self.start_gif_label = QLabel(self)
        self.start_gif_label.setGeometry(400, 560, 140, 140)
        self.start_gif_label.setMovie(self.start_gif)
        self.start_gif_label.setScaledContents(True)
        self.start_gif_label.hide()

        # apply stop button image to main UI
        self.stop_image = QPixmap("./images/stop.png")
        self.stop_processed_image = self.stop_image.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.stop_btn = QPushButton(self)
        self.stop_btn.setIcon(QIcon(self.stop_processed_image))
        self.stop_btn.setIconSize(self.stop_processed_image.size())
        self.stop_btn.move(650,560)
        self.stop_btn.clicked.connect(self.stop_threads)

        # apply link button to main UI
        self.link_btn = QPushButton(self)
        self.link_btn.setGeometry(830, 600, 350, 50)
        self.link_btn.setStyleSheet("border-image:url(./images/server.png)")
        self.link_btn.clicked.connect(self.open_url)

        #main UI
        self.setGeometry(400, 200, 1200, 700)
        self.setStyleSheet("background : white;")

        # Thread synchronization
        self.mutex = QMutex()

    def start_threads(self):
        self.start_btn.hide()
        self.start_gif_label.show()
        self.start_gif.start()
        QMessageBox.about(self,'차량 상태',f'★ENGINE START ★')
        self.start_gif.stop()
        self.background_label.setStyleSheet("background : white;")

        # show Driver video to main UI
        self.thread_Driver = VideoThread('./videos/Driver.mp4', self.mutex)
        self.thread_Driver.change_pixmap_signal.connect(self.update_driver_image)
        self.thread_Driver.start()

        # show Car video to main UI
        #self.thread_Car = VideoThread('http://192.168.100.146:5000/video_feed', self.mutex)
        self.Car_label.setStyleSheet("background : white;")
        self.thread_Car = VideoThread('./videos/Car.mp4', self.mutex)
        self.thread_Car.change_pixmap_signal.connect(self.update_car_image)
        self.thread_Car.start()

        # show Processing video to main UI
        self.Processing_label.setStyleSheet("background : white;")
        self.thread_Processing = VideoThread('./videos/Server.mp4', self.mutex)
        self.thread_Processing.change_pixmap_signal.connect(self.update_processing_image)
        self.thread_Processing.start()

    def stop_threads(self):
        if hasattr(self, 'thread_Driver') and self.thread_Driver.isRunning():
            self.thread_Driver.stop()
        if hasattr(self, 'thread_Car') and self.thread_Car.isRunning():
            self.thread_Car.stop()
        if hasattr(self, 'thread_Processing') and self.thread_Processing.isRunning():
            self.thread_Processing.stop()

        self.start_btn.show()
        self.start_gif_label.hide()
        QMessageBox.about(self,'차량 상태',f'★ENGINE STOP ★')

    def update_driver_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.Driver_label.setPixmap(qt_img)

    def update_car_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.Car_label.setPixmap(qt_img)

    def update_processing_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.Processing_label.setPixmap(qt_img)

    # Convert from an opencv image to QPixmap
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_image.shape
        bytes_per_line = channel * width
        convert_to_Qt_format = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        resized_img = convert_to_Qt_format.scaled(300, 450)

        return QPixmap.fromImage(resized_img)

    def open_url(self):
           url = QUrl('http://54.175.8.12')
           QDesktopServices.openUrl(url)

"""
-----------------------------------------------------------------------------------------------------------------------------
"""

class VideoThread(QThread):
    change_pixmap_signal = Signal(object)
    def __init__(self, video_path, mutex):
        super().__init__()
        self.video_path = video_path
        self.mutex = mutex
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while self.running:
            self.mutex.lock()
            ret, cv_img = cap.read()
            self.mutex.unlock()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
                self.msleep(20)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cap.release()

    def stop(self):
        self.running = False

"""
-----------------------------------------------------------------------------------------------------------------------------
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    first_window = FirstWindow()
    first_window.show()
    sys.exit(app.exec_())
