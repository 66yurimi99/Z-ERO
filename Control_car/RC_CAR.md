# RC Car Control
Self-driving RC CAR Using Segmentation Area & Detected Object Information

## Results
### 1. Send Video from Raspberry Pi to PC
```python
_, buffer = cv2.imencode('.jpg', frame)
frame_bytes = buffer.tobytes()
yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
def get_response(self):
    return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
```    

### 2. Get Data using HTTP & Parsing
```python
### Get data
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        return None

### data Parsing
if data:
    print(f"The data is: {data}")
    tem = data.split(',')
    with mutex:
        isCar = int(tem[0])
        Driver_state = int(tem[1])
        obj = int(tem[2])
        if len(tem) > 3:
            theta = float(tem[3])
        else:#exception handle
            theta = 20.0
else:
    print("Can't read")
```

### 3. Self-driving Algorithm
```python
self.vel = self.default_vel* abs(self.theta)/90 * self.obj_state
if self.vel>=100:
    self.vel = 99
elif self.vel<70 and self.obj_state != 0:
    self.vel = 70
if self.state == "straight":
    self.left_wheel.ChangeDutyCycle(self.vel)
    self.right_wheel.ChangeDutyCycle(self.vel)
elif self.state == "a little right":
    self.left_wheel.ChangeDutyCycle(self.vel)
    self.right_wheel.ChangeDutyCycle(0.8*self.vel)
elif self.state == "right":
    self.left_wheel.ChangeDutyCycle(self.vel)
    self.right_wheel.ChangeDutyCycle(0.5 * self.vel)
elif self.state == "a little left":
    self.left_wheel.ChangeDutyCycle(0.8*self.vel)
    self.right_wheel.ChangeDutyCycle(self.vel)
elif self.state == "left":
    self.left_wheel.ChangeDutyCycle(0.5 * self.vel)
    self.right_wheel.ChangeDutyCycle(self.vel)
```

## Settings

### 1. Pin Configuration
  
  <img src="https://github.com/66yurimi99/Z-ERO/assets/86766617/2e22b351-6af7-4a81-ba6a-981cb0e8dfd8" width="500" height="300">

```python
## GPIO motor pin
self.GPIO_Right = 12
self.GPIO_Left = 13
##GPIO LED pin
self.GPIO_Left_LED = 5
self.GPIO_Right_ELD = 6
```      

### 2. Installation
```python
signals==0.0.2
RPi.GPIO==0.7.0
requests==2.25.1
thread==0.1.2
responses==0.12.1
```


