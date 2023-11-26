import glob
import time
import cv2
import numpy as np
import openvino as ov
from openvino.inference_engine import IECore

# 모델 파일 경로
detect_xml = 'detect.xml'
detect_bin = 'detect.bin'
classi_xml = 'classi.xml'
classi_bin = 'classi.bin'
images_path_O = "O/*.jpg"
images_path_X = "X/*.jpg"

ie = IECore()

O_cnt = 0
X_cnt = 0
total_FPS = 0
i = 1

# Read Model
detect_net = ie.read_network(model=detect_xml, weights=detect_bin)
classi_net = ie.read_network(model=classi_xml, weights=classi_bin)

# PreProccessing(Batch size = 1)
input_layer_name_1 = next(iter(detect_net.input_info))
input_shape_1 = detect_net.input_info[input_layer_name_1].input_data.shape
input_shape_1[0] = 1
detect_net.reshape({input_layer_name_1: input_shape_1})

input_layer_name_2 = next(iter(classi_net.input_info))
input_shape_2 = classi_net.input_info[input_layer_name_2].input_data.shape
input_shape_2[0] = 1
classi_net.reshape({input_layer_name_2: input_shape_2})
    
# Load Model
detect_exec_net = ie.load_network(network=detect_net, device_name='CPU', num_requests=1)
classi_exec_net = ie.load_network(network=classi_net, device_name='GPU', num_requests=1)

# 이미지 파일이 있는 디렉토리에서 파일 목록을 가져옴
image_files_O = glob.glob(images_path_O)
image_files_X = glob.glob(images_path_X)

# 이미지 파일을 순회하면서 열기
for image_path in image_files_O:
    start_time = time.time()
    # 이미지 파일을 열기
    image = cv2.imread(image_path)
    if image is None:
        raise
    cv2.imshow("aaa", image)
    images = cv2.resize(image, (864, 864))

    # Change color order if needed (BGR to RGB or vice versa)
    image = images[..., ::-1]
    # Change data layout to HWC
    image = image.transpose((2, 0, 1))
    input_tensor = np.expand_dims(image, 0)

    results = detect_exec_net.infer(inputs={input_layer_name_1: image})

    for result in results['boxes']:
        if result[0][4] > 0.95:
            img_crop = images[int(result[0][1]):int(result[0][3]),int(result[0][0]):int(result[0][2])]
            img_crop = cv2.resize(img_crop, (224, 224))
            img_crop = img_crop[..., ::-1]
            img_crop = img_crop.transpose((2, 0, 1))
            input_tensor = np.expand_dims(img_crop, 0)
            
            results_1 = classi_exec_net.infer(inputs={input_layer_name_2: img_crop})
            
            end_time = time.time() 
            total_FPS += 1 / (end_time - start_time)

            x = results_1['logits'][0]
            eps: float = 1e-9
            x = np.exp(x - np.max(x))
            x = x / (np.sum(x) + eps)
            if x[0] > 0.75:
                O_cnt += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for image_path in image_files_X:
    start_time = time.time()
    # 이미지 파일을 열기
    image = cv2.imread(image_path)
    if image is None:
        raise
    images = cv2.resize(image, (864, 864))

    # Change color order if needed (BGR to RGB or vice versa)
    image = images[..., ::-1]
    # Change data layout to HWC
    image = image.transpose((2, 0, 1))
    input_tensor = np.expand_dims(image, 0)

    results = detect_exec_net.infer(inputs={input_layer_name_1: image})

    for result in results['boxes']:
        if result[0][4] > 0.95:
            img_crop = images[int(result[0][1]):int(result[0][3]),int(result[0][0]):int(result[0][2])]
            img_crop = cv2.resize(img_crop, (224, 224))
            img_crop = img_crop[..., ::-1]
            img_crop = img_crop.transpose((2, 0, 1))
            input_tensor = np.expand_dims(img_crop, 0)
            
            results_1 = classi_exec_net.infer(inputs={input_layer_name_2: img_crop})
            
            end_time = time.time() 
            total_FPS += 1 / (end_time - start_time)

            x = results_1['logits'][0]
            eps: float = 1e-9
            x = np.exp(x - np.max(x))
            x = x / (np.sum(x) + eps)
            if x[1] > 0.75:
                X_cnt += 1

ave_FPS = total_FPS / 200
O_accuracy = O_cnt / 100
X_accuracy = X_cnt / 100
print("FPS: ", ave_FPS)
print("O_accuracy: ", O_accuracy)
print("X_accuracy: ", X_accuracy)