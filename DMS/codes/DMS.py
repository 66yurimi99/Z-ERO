import time
import cv2
import requests
import threading
import numpy as np
from OV import OpenVINO

class DMS:
    def __init__(self):
        self.ov = OpenVINO()
        self.pre_flag = 0
        self.cnt = 0
        self.blink_start = 0
        self.blink_end = 0
        self.close_start = 0
        self.close_end = 0
        self.cur_status = 0
        self.pre_status = 0
        self.car = 'car'
        self.number = 'number'
        self.info_car = 0
        self.info_number = ''
        self.get_url = 'http://54.175.8.12/db_get.php?'
        self.set_url = 'http://54.175.8.12/db_set.php?driver='
        #운전자 초기상태: 0
        self.set_request_driver(self.cur_status)
        # URL에서 데이터를 읽어오는 스레드 초기화
        self.url_thread = threading.Thread(target=self.read_car_and_number_data)
        # 데몬 스레드로 설정하여 메인 프로그램이 종료될 때 함께 종료되도록 함
        self.url_thread.daemon = True
        # 스레드 시작
        self.url_thread.start()
        
    def read_car_and_number_data(self):
        while True:
            self.info_car = self.get_request(self.car)
            time.sleep(1)

    def get_request(self, info):
        get_url_with_info = f"{self.get_url}{info}"
        info = requests.get(get_url_with_info)
        datas = info.text.split(",")
        return datas[0]

    def set_request_driver(self, info):
        get_url_with_info = f"{self.set_url}{info}"
        info = requests.get(get_url_with_info)
        datas = info.text.split(",")
        return datas[0]

    def process_frame(self, image):
        cur_flag = 0
        status = 0
        start_time = time.time()  # FPS 측정 시작

        results, image = self.ov.detect_blink(image, self.ov.input_layer_name_1)
        for result in results['boxes']:
            if result[0][4] > 0.95:
                results_1 = self.ov.classify_eye_state(image, self.ov.input_layer_name_2, result)
                end_time = time.time()  # FPS 측정 종료

                FPS = 1 / (end_time - start_time)
                x = results_1['logits'][0]
                eps: float = 1e-9
                x = np.exp(x - np.max(x))
                x = x / (np.sum(x) + eps)
                if x[0] > 0.6:
                    cur_flag = 0
                elif x[1] > 0.6:
                    cur_flag = 1

        #print("FPS: ", FPS)
        #print(cur_flag)

        close_time, blink_time = 0, 0
        if self.pre_flag == 0 and cur_flag == 1:
            self.blink_start = time.time()
            self.close_start = time.time()
        elif self.pre_flag == 1 and cur_flag == 0:
            self.blink_end = time.time()
        elif self.pre_flag == 0 and cur_flag == 0:
            self.blink_start = 0
            self.blink_end = 0
        elif self.pre_flag == 1 and cur_flag == 1:
            self.close_end = time.time()
        close_time = self.close_end - self.close_start
        blink_time = self.blink_end - self.blink_start

        if blink_time <= 0.3 and blink_time > 0:
            self.cnt = 0
            #print("멀쩡")
        elif blink_time > 0.3:
            self.cnt += 1
            print(self.cnt)
            if self.cnt >= 3:
                status = 1
                print("졸음!")
        if close_time >= 3:
            status = 2
            print("잠듬!")

        self.pre_flag = cur_flag
        print(cur_flag)
        return status, image

    def run(self):
        cap = cv2.VideoCapture(0)
        open_start = 0
        open_end = 0
        open_flag = False
        
        #import pdb; pdb.set_trace()
        while True:
            open_time = 0
            ret, image = cap.read()
            if not ret:
                print("웹캠에서 프레임을 읽을 수 없습니다.")
                break
            if (self.info_car == '1'):
                self.cur_status, image = self.process_frame(image)
                #send_status(0,1,2)
                if self.pre_status == 0 and self.cur_status > 0:
                    self.set_request_driver(self.cur_status)
                elif self.pre_status > 0 and self.cur_status == 0:
                    open_start = time.time()
                    open_flag = True
                open_end = time.time()
                open_time = open_end - open_start
                if open_time >= 5 and open_flag == True:
                    self.set_request_driver(self.cur_status)
                    open_flag = False
                #send_frame_to_QT(image)
                #운전자 상태, 영상(크롭?)
                self.pre_status = self.cur_status
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    dms = DMS()
    dms.run()
