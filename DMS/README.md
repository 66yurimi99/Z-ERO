# DMS(Driver Monitoring System)
운전자 상태를 확인하기 위한 시스템을 구축합니다.

## Results
### 1. 운전자 상태 확인을 위한 눈감음 판단 모델
- OTX(OpenVINO Training Extensions)로 모델 training
- Face Detection 모델로 `mobilenetv2_ssd` 사용
  - `detect.xml`: 모델파일
  - `detect.bin`: 가중치파일
- Eyes close Classification 모델로 `MobileNet-V3-large-1x` 사용
  - `classi.xml`: 모델파일
  - `classi.bin`: 가중치파일
 
### 2. 눈감음 시간을 통한 운전자 졸음 상태 확인
- 눈을 감은 채 지속되는 시간이 0.3초 이하면 정상 눈 상태
- 지속시간이 0.3초를 초과하고 눈을 뜨면 이상 상태로 보고 `cnt` 증가
- `cnt`가 3 이상이면 졸음 상태로 판단
- 눈 감음 지속시간이 3초 이상이면 잠듬 상태로 판단
<br>

- `status = 0 (defalut)`: 정상
- `status = 1`: 졸음
- `status = 2`: 잠듬

```python
close_time, blink_time = 0, 0
if self.pre_flag == 0 and cur_flag == 1: # 눈 감음
    self.blink_start = time.time()
    self.close_start = time.time()
elif self.pre_flag == 1 and cur_flag == 0: # 눈 뜸
    self.blink_end = time.time()
elif self.pre_flag == 0 and cur_flag == 0: # 눈 뜨고 있음
    self.blink_start = 0
    self.blink_end = 0
elif self.pre_flag == 1 and cur_flag == 1: # 눈 감고 있음
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
```
### 3. 운전자 상태 정보 WebServer DB를 통한 통신

### 4. OTX 모델 성능 비교 및 dlib 모델 비교
#### Face detector Training 결과
|model name|Device|Accuracy|FPS|Batch size|Learning rate|Epoch|
|----|----|----|----|----|----|----|
|mobilenet-ATSS| CPU | 0.76(70%) / 0.28(80%) / 0.0(90%) | 19 | 8 | 0.004 | 200 |
|mobilenet-ATSS| GPU | 0.76(70%) / 0.32(80%) / 0.0(90%) | 9 | 8 | 0.004 | 200 |
|SSD| CPU | 1.0(90%) / 1.0(99%) | 25 | 8 | 0.01 | 200 |
|SSD| GPU | 1.0(90%) / 1.0(99%) | 10 | 8 | 0.01 | 200 |
|YOLOX| CPU | 1.0(80%) / 0.96(88%) / 0.76(90%) | 44 | 8 | 0.0002 | 200 |
|YOLOX| GPU | 1.0(80%) / 0.96(88%) / 0.72(90%) | 38 | 8 | 0.0002 | 200 |
#### Eyes close classification Training 결과
|model name|Device|Accuracy|FPS|Batch size|Learning rate|Epoch|
|----|----|----|----|----|----|----|
|EfficientNet-B0| GPU | O: 0.92(70%) / 0.92(80%) / 0.89(90%)<br>X: 0.98(70%) / 0.95(80%) / 0.94(90%) | 145 | 64 | 0.0049 | 90 |
|EfficientNet-V2-S| GPU | O: 0.96(70%) / 0.95(80%) / 0.94(90%)<br>X: 0.99(70%) / 0.99(80%) / 0.99(90%) | 183 | 64 | 0.0058 | 90 |
|MobileNet-V3-large-1x| GPU | O: 1.0(77%) / 0.99(80%) / 0.99(90%)<br>X: 1.0(75%) / 0.99(80%) / 0.99(90%) | 55 | 64 | 0.0071 | 90 |
- SSD(CPU) + MobileNet-V3-large-1x(GPU) 선정

### dlib basic model vs Trained model
|model sets|FPS|O_Accuracy|X_Accuracy|
|----|----|----|----|
|dlib basic models| 9 | 0.32 | 0.16 |
|Trained models| 26 | 1.0 | 1.0 |
- dlib: frontal face detector, 68 facial landmarks
- trained model이 얼굴 감지 및 눈 감음 분류에서 더 높은 성능을 보여줌

## Setting
### Install requirements
- Python 설치
  - ```shell
    $ apt-get install python==3.10.12
    ```
- Python 환경 설치
  - ```shell
    $ pip install requirements.txt
    ```
## Explain
- `dms.py` : DMS 실행용 모듈
- `ov.py` : 모델 Inferencing용 모듈
- `main.py` : 실행 메인 파일
- `test_code.py` : 모델 테스트용 코드