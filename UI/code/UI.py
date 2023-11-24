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
        self.input_CarNumber.setText('차량 번호를 입력해주세요.')
        self.input_CarNumber.setStyleSheet("color: black; border: 3px solid black;")
        self.input_CarNumber.setAlignment(Qt.AlignCenter)
        self.input_CarNumber.setGeometry(450,500,300,50)
        self.input_CarNumber.mousePressEvent = self.clearText

        #apply Next button image to main UI
        next_btn = QPushButton(self)
        next_btn.setGeometry(550, 550, 100, 100)
        next_btn.setStyleSheet("border-image:url(./images/next.png)")
        next_btn.clicked.connect(self.showSecondWindow)

        #show main UI
        self.setGeometry(400, 200, 1200, 700)
        self.setStyleSheet("background : white;")
        self.show()

    def sendCarNumber(self):
        #send Car Number to server
        CarNumber=self.input_CarNumber.text()
        #url=f'http://54.175.8.12/db.php?number={CarNumber}'
        #response = requests.get(url)
        QMessageBox.about(self,'차량 등록',f'★ [{CarNumber}] 등록 완료 ★')

        #Todo
        #DMS한테 차량번호 넘겨주기
    def clearText(self, event):
            self.input_CarNumber.clear()
            self.input_CarNumber.selectAll()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.sendCarNumber()
            event.accept()

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
        self.initUI()

    def initUI(self):
        # Set font and size for labels
        inform_Driver = QLabel('Driver',self)
        inform_Car = QLabel('Car',self)
        inform_Processing = QLabel('Processing',self)

        font = QFont()
        font.setPointSize(20)
        inform_Driver.setFont(font)
        inform_Car.setFont(font)
        inform_Processing.setFont(font)

        # Set styles for labels
        inform_Driver.setStyleSheet("color: red;" "border-style: solid;")
        inform_Car.setStyleSheet("color: green;" "border-style: solid;")
        inform_Processing.setStyleSheet("color: blue;" "border-style: solid;")

        inform_Driver.move(150, 40)
        inform_Car.move(560, 40)
        inform_Processing.move(930, 40)

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

        # apply start button image to main UI
        start_image = QPixmap("./images/start.png")
        start_processed_image = start_image.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.start_btn = QPushButton(self)
        self.start_btn.setIcon(QIcon(start_processed_image))
        self.start_btn.setIconSize(start_processed_image.size())
        self.start_btn.move(30,560)
        self.start_btn.clicked.connect(self.start_threads)

        # apply stop button image to main UI

        stop_image = QPixmap("./images/stop.png")
        stop_processed_image = stop_image.scaled(130, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.stop_btn = QPushButton(self)
        self.stop_btn.setIcon(QIcon(stop_processed_image))
        self.stop_btn.setIconSize(stop_processed_image.size())
        self.stop_btn.move(210,560)
        self.stop_btn.clicked.connect(self.stop_threads)

        # apply link button to main UI
        self.link_btn = QPushButton(self)
        self.link_btn.setGeometry(700, 600, 400, 50)
        self.link_btn.setStyleSheet("border-image:url(./images/server.png)")
        self.link_btn.clicked.connect(self.open_url)

        #main UI
        self.setGeometry(400, 200, 1200, 700)
        self.setStyleSheet("background : white;")

        # Thread synchronization
        self.mutex = QMutex()

    def start_threads(self):

        QMessageBox.about(self,'차량 상태',f'★ENGINE START ★')

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

        # Stop Car video thread
        if hasattr(self, 'thread_Car') and self.thread_Car.isRunning():
            self.thread_Car.stop()

        # Stop Processing video thread
        if hasattr(self, 'thread_Processing') and self.thread_Processing.isRunning():
            self.thread_Processing.stop()

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
