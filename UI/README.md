# UI
자동차 주행 환경에 대한 사용자 UI를 구축합니다.

## Settings
- Qtcreator 설치
    ```shell
    sudo apt install qtcreator 
    ```
- 필요한 패키지 설치
    ```shell
    pip install pyside2
    pip install opencv-python-headless
    pip install requests
    ```

## Function
### 1. 차량 번호 등록 기능
다음 요청들을 통해 차량 번호를 등록하고 서버에 전송할 수 있습니다. (`HTTP/GET`)
- 차량 등록 
    ```python
    def initUI(self):
    #Input Car Number to main UI
        self.input_CarNumber = QLineEdit(self)
        self.input_CarNumber.setText('차량 번호를 입력해주세요 (ENTER)')
        self.input_CarNumber.setStyleSheet("color: black; border: 3px solid black;")
        self.input_CarNumber.setAlignment(Qt.AlignCenter)
        self.input_CarNumber.setGeometry(450,500,300,50)
        self.input_CarNumber.mousePressEvent = self.clearText

    def sendCarNumber(self):
    CarNumber=self.input_CarNumber.text()
    QMessageBox.about(self,'차량 등록',f'★ [{CarNumber}] 등록 완료 ★')
    ```
- 등록된 차량 번호 서버에 전송
    ```python
    url=f'http://54.175.8.12/db_set.php?number={CarNumber}'
    response = requests.get(url)
    ```

### 2. Start 버튼 클릭 시 Thread 동작 
서버에 자동차의 상태 "시동 on"을 전송하고 각각의 Thread에서 정보를 읽어옵니다.
- 자동차의 시동 상태 정보를 서버에 전송하고 시작 화면 setting
    ```python
    def start_threads(self):

        url=f'http://54.175.8.12/db_set.php?car={1}'
        response = requests.get(url)

        self.start_btn.hide()
        self.start_gif_label.show()
        self.start_gif.start()
        QMessageBox.about(self,'차량 상태',f'★ENGINE START ★')
        self.start_gif.stop()
        self.background_label.setStyleSheet("background : white;")
    ```
- 각각의 Thread에서 정보를 읽어옵니다.
    ```python
    # show Driver video to main UI
    #self.thread_Driver = VideoThread('http://{Driver_Path}/video_feed', self.mutex)
    self.thread_Driver = VideoThread('./videos/Driver.mp4', self.mutex)
    self.thread_Driver.change_pixmap_signal.connect(self.update_driver_image)
    self.thread_Driver.start()

    # show Car video to main UI
    #self.thread_Car = VideoThread('http://{Car_Path}/video_feed', self.mutex)
    self.Car_label.setStyleSheet("background : white;")
    self.thread_Car = VideoThread('./videos/Car.mp4', self.mutex)
    self.thread_Car.change_pixmap_signal.connect(self.update_car_image)
    self.thread_Car.start()

    # show Processing video to main UI
    #self.thread_Processing = VideoThread('http://192.168.100.146:5000/video_feed', self.mutex)
    self.Processing_label.setStyleSheet("background : white;")
    self.thread_Processing = VideoThread('./videos/Server.mp4', self.mutex)
    self.thread_Processing.change_pixmap_signal.connect(self.update_processing_image)
    self.thread_Processing.start()
    ```

### 3. Stop 버튼 클릭 시 Thread 종료
서버에 자동차의 상태 "시동 off"을 전송하고 Thread를 종료합니다.
```python
def stop_threads(self):
url=f'http://54.175.8.12/db_set.php?car={0}'
response = requests.get(url)

if hasattr(self, 'thread_Driver') and self.thread_Driver.isRunning():
    self.thread_Driver.stop()
if hasattr(self, 'thread_Car') and self.thread_Car.isRunning():
    self.thread_Car.stop()
if hasattr(self, 'thread_Processing') and self.thread_Processing.isRunning():
    self.thread_Processing.stop()

self.start_btn.show()
self.start_gif_label.hide()
QMessageBox.about(self,'차량 상태',f'★ENGINE STOP ★')
```

### 4. Link 버튼 클릭 시 서버 홈페이지 접속
```python
def initUI(self):
    # apply link button to main UI
    self.link_btn = QPushButton(self)
    self.link_btn.setGeometry(1375, 600, 350, 50)
    self.link_btn.setStyleSheet("border-image:url(./images/server.png)")
    self.link_btn.clicked.connect(self.open_url)

def open_url(self):
           url = QUrl('http://54.175.8.12')
           QDesktopServices.openUrl(url)

```

