import cv2
import numpy as np
from openvino.inference_engine import IECore

class OpenVINO:
    def __init__(self):
        self.ie = IECore()

        self.detect_net, self.input_layer_name_1 = self.load_model('../model/detect.xml', 'model/detect.bin', 'CPU')
        self.classi_net, self.input_layer_name_2 = self.load_model('../model/classi.xml', 'model/classi.bin', 'GPU')

    def load_model(self, xml_path, bin_path, device):
        net = self.ie.read_network(model=xml_path, weights=bin_path)
        input_layer_name = next(iter(net.input_info))
        input_shape = net.input_info[input_layer_name].input_data.shape
        input_shape[0] = 1
        net.reshape({input_layer_name: input_shape})
        exec_net = self.ie.load_network(network=net, device_name=device, num_requests=1)
        return exec_net, input_layer_name

    def detect_blink(self, image, input_layer_name_1):
        images = cv2.resize(image, (864, 864))
        image = images[..., ::-1]
        image = image.transpose((2, 0, 1))
        input_tensor = np.expand_dims(image, 0)
        result = self.detect_net.infer(inputs={input_layer_name_1: image})
        return result, image  # 결과 반환

    def classify_eye_state(self, image, input_layer_name_2, result):
        image = image.transpose((2, 0, 1))
        image = image.transpose((2, 0, 1))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        images = image[int(result[0][1]):int(result[0][3]), int(result[0][0]):int(result[0][2])]
        cv2.imshow('DMS', images)
        image = cv2.resize(images, (224, 224))
        #cv2.imshow('DMS', image)
        image = image[..., ::-1]
        image = image.transpose((2, 0, 1))
        input_tensor = np.expand_dims(image, 0)
        results_1 = self.classi_net.infer(inputs={input_layer_name_2: image})
        return results_1  # 결과 반환
