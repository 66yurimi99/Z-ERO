# LCA(Lane Centering Assistant)
Lane Detection 을 위한 시스템을 구축합니다.

## Results
### 1. Lane Detection을 위한 모델 선정
- OTX(OpenVINO Training Extensions)로 모델 training
- Lane Detection 모델로 아래 3가지 모델 중 ` MaskRCNN-EfficientNetB2B` 사용
   1. MaskRCNN-EfficientNetB2B
   2. MaskRCNN-ResNet50
   3. MaskRCNN-SwinT-FP16
  - FPS issue로 인하여 PC 환경 변경 및 optimize 진행

### 2. annotation을 통한 segmentation 진행
- annotation을 통해 Lane 위 segmentation 진행

```python
#(IP address is raspberry pi) 
    cap = cv2.VideoCapture("http://10.10.141.62:5000/video_feed") 
    while (cap.isOpened()):
        ret, img = cap.read()
        if not ret:
            print("can't read vid...")
            break
        # Inference
        predictions = core_model(img)
        frame_meta = {"original_shape": img.shape}
        # Post-processing
        annotations = convert_to_annotation(predictions, frame_meta)
```
### 3. RC 카 제어를 위한 theta 알고리즘 구현    

```python
def cal_dist(pt1, pt2):
    #.../
#dist1이 항상 화면의 수선 벡터로 고정합시다(각의 음, 양 출력)
def cal_theta(dist1, dist2,dist3): 
    #제2코사인법칙
    cos_t = (pow(dist1,2)+pow(dist2,2)-
             pow(dist3,2))/(2*dist1*dist2)
    #radian-> degree로 바꿈 
    theta = math.acos(cos_t)* (180/math.pi)
```

### 4. 운전자 상태 정보 Web DB를 통한 통신

```python
def thread_function_server():
    while True:
        global theta
        p = request.get(f'http://54.175.8.12/control.php?direction={theta}')

def thread_function_getdriver():
    global driver
    while is_bool:
        get = requests.get(f'http://54.175.8.12/db_get.php?driver')
        temp= get.text
        driver = temp.split(",")[0]
        time.sleep(1)
```

## Setting
### Install requirements
   ```sh
   sudo apt install python3-pip
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

# How to run
   ```sh
   python3 test.py
   ```
