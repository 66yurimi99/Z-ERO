import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import *
from PyQt5 import uic


# Start Window
class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI() 

    def initUI(self):
        #apply Project name image to main UI
        title_load = QPixmap('C:\\PyQT Example\\Zero\\images\\Z_ERO.png') 
        title_img = QLabel(self) 
        title_img.setPixmap(title_load) 
        title_img.setGeometry(50, 100, title_load.width(), title_load.height())
           
        #apply Next button image to main UI
        next_btn = QPushButton(self)
        next_btn.setGeometry(420, 550, 100, 100)
        next_btn.setStyleSheet("border-image: url(C:/PyQT Example/Zero/images/next.png)")
        next_btn.clicked.connect(self.showSecondWindow)

        #apply logo image to main UI
        self.setWindowTitle('Intel Project')
        self.setGeometry(500, 300, title_load.width(), 700)
        self.setStyleSheet("background : white;")
        logo_pixmap = QPixmap('C:\\PyQT Example\\Zero\\images\\intel.png')
        resized_logo = logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        self.setWindowIcon(QIcon(resized_logo))
        self.show()

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
        
        self.disply_width = 100
        self.display_height = 100  
        
        # set Driver video to main UI
        self.Driver_label = QLabel(self) 
        self.Driver_label.resize(300, 550)
        self.Driver_label.setStyleSheet("background : black;")
        self.Driver_label.move(0, 0)
        
        # set Car video to main UI
        self.Car_label = QLabel(self) 
        self.Car_label.resize(300, 550)
        self.Car_label.setStyleSheet("background : black;")
        self.Car_label.move(300, 0)

        # set Processing video to main UI
        self.Processing_label = QLabel(self) 
        self.Processing_label.resize(300, 550)
        self.Processing_label.setStyleSheet("background : black;")
        self.Processing_label.move(600, 0)

        # Thread synchronization
        self.mutex = QMutex()

        # apply start button image to main UI
        self.start_btn = QPushButton(self)
        self.start_btn.setGeometry(300, 600, 100, 70)
        self.start_btn.setStyleSheet("border-image: url(C:/PyQT Example/Zero/images/start.png)")
        self.start_btn.clicked.connect(self.start_threads)

        # apply stop button image to main UI
        self.stop_btn = QPushButton(self)
        self.stop_btn.setGeometry(500, 600, 100, 70)
        self.stop_btn.setStyleSheet("border-image: url(C:/PyQT Example/Zero/images/pause.png)")
        self.stop_btn.clicked.connect(self.stop_threads)

        # apply logo image to main UI
        self.setGeometry(500, 300, 900, 700)
        self.setStyleSheet("background : white;")
        self.setWindowTitle('Intel Project')
        logo_pixmap = QPixmap('C:\\PyQT Example\\Zero\\images\\intel.png')
        resized_logo = logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        self.setWindowIcon(QIcon(resized_logo))

    def start_threads(self):
        # show Driver video to main UI
        self.thread_Driver = VideoThread('C:\\PyQT Example\\Zero\\videos\\Driver.mp4', self.mutex)
        self.thread_Driver.change_pixmap_signal.connect(self.update_driver_image)
        self.thread_Driver.start()

        # show Car video to main UI
        self.thread_Car = VideoThread('C:\\PyQT Example\\Zero\\videos\\Car.mp4', self.mutex) 
        self.thread_Car.change_pixmap_signal.connect(self.update_car_image)
        self.thread_Car.start()

        # show Processing video to main UI
        self.thread_Processing = VideoThread('C:\\PyQT Example\\Zero\\videos\\Server.mp4', self.mutex) 
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
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        #p = convert_to_Qt_format.scaled(300, 300, Qt.KeepAspectRatio) Qt.KeepAspectRatio 가로와 세로의 비율을 유지
        p = convert_to_Qt_format.scaled(300, 550)
        return QPixmap.fromImage(p)

"""
-----------------------------------------------------------------------------------------------------------------------------
"""

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(object)

    def __init__(self, video_path, mutex):
        super().__init__()
        self.video_path = video_path
        self.mutex = mutex
        self.running = True  # Flag to control the loop

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while self.running:
            self.mutex.lock()
            ret, cv_img = cap.read()
            self.mutex.unlock()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            else:
                # replay when the video is ended
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
    sys.exit(app.exec_()) #Event Loop 