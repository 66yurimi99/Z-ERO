"""Demo based on ModelAPI."""
# Copyright (C) 2021-2023 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#

import os
import sys
from urllib import request, response
import cv2
import numpy as np
import math
import requests
import threading

from typing import Any, Dict, List
from openvino.runtime import Core
from openvino.model_api.adapters import OpenvinoAdapter, create_core
from openvino.model_api.models import Model
from utils.polygon import Point, Polygon
from utils.openvino_models import OTXMaskRCNNModel
theta = 20

# Define Labels
labels = ['1st', '2nd']

# Load AI model and define the device for AI inference
model_adapter = OpenvinoAdapter(
    create_core(), "./model/openvino.xml", device="CPU"
)

# Define the params
model_parameters = {
    'result_based_confidence_threshold': True, # result_based_confidence_threshold of config.json
    'confidence_threshold': 0.8999999761581421, # confidence_threshold of config.json
    'labels': []
}

# Create an OpenVINO model
core_model = Model.create_model(
    model_adapter,
    "OTX_MaskRCNN", # "type_of_model" in config.json
    model_parameters,
    preload=True,
)
'''
def read_cam():
    cap = cv2.VideoCapture("http://192.168.100.146:5000/video_feed")  #(IP address is raspberry pi)
    w = 640  # 1280#1920
    h = 480  # 720#1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    return cap
'''
def cal_dist(pt1, pt2):
    dist_x = pow(pt1[0]-pt2[0],2)
    dist_y = pow(pt1[1]-pt2[1],2)
    dist = math.sqrt(dist_x + dist_y)
    return dist

def cal_theta(dist1, dist2,dist3): #dist1이 항상 화면의 수선 벡터로 고정합시다(각의 음, 양 출력)
    cos_t = (pow(dist1,2)+pow(dist2,2)-pow(dist3,2))/(2*dist1*dist2) #제2코사인법칙
    theta = math.acos(cos_t)* (180/math.pi) #radian-> degree로 바꿈
    return theta # 근데 절대적 각도라 미세 처리 필요함(작성하는중)

def get_vector(pt1, pt2):
    #import pdb; pdb.set_trace()
    return (pt1[0]-pt2[0],pt1[1]-pt2[1])
'''
def outer_product(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.outer(vec1, vec2)
'''
def convert_to_annotation(
    predictions: tuple, metadata: Dict[str, Any]
):
    annotations = []

    for score, class_idx, box, mask in zip(*predictions):
        mask = mask.astype(np.uint8)
        contours, hierarchies = cv2.findContours(
            mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )
        if hierarchies is None:
            continue

        #print("box = {}".format(box))
        for contour, hierarchy in zip(contours, hierarchies[0]):
            if hierarchy[3] != -1:
                continue
            if len(contour) <= 2 or cv2.contourArea(contour) < 1.0:
                continue
            contour = list(contour)
            points = [
                Point(
                    x=point[0][0] / metadata["original_shape"][1],
                    y=point[0][1] / metadata["original_shape"][0],
                )
                for point in contour
            ]
            polygon = Polygon(points=points)
            annotation = (polygon, labels[int(class_idx) - 1], float(score))
            annotations.append(annotation)

    return annotations

def thread_function_server():
    while True:
        global theta
        print(theta)
        response = requests.get(f'http://54.175.8.12/control.php?direction={theta}')
        #import pdb; pdb.set_trace()
        

def thread_function_model():
    global theta
    cap = cv2.VideoCapture("http://10.10.141.62:5000/video_feed")  #(IP address is raspberry pi) 
    width = 1280
    height = 720
    ###middle point & btm point
    mid_pt = (int(width//2), int(height//2))
    btm_pt = (int(width//2), height)
    while (cap.isOpened()):
        #img = cv2.imread("test.jpg")
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        ret, img = cap.read()
        if not ret:
            print("can't read vid...")
            break
        # Inference
        predictions = core_model(img)
        frame_meta = {"original_shape": img.shape}
        #print("predictions = {}".format(predictions))
        #print("frame_meta = {}".format(frame_meta))


        # Post-processing
        annotations = convert_to_annotation(predictions, frame_meta)

        # Display
        alpha_shape = 100 / 256
        alpha_labels = 153 / 256
        base_color = [ (255, 0, 53),
                    (0, 0, 255) ]
        label_offset_box_shape = 0
        num_annotations = 0

        ret_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        mid_x=0
        mid_y=0
        for annotation in annotations:
            if(annotation[2]>0.90):
                contours = np.array(
                    [
                        [point.x * img.shape[1], point.y * img.shape[0]]
                        for point in annotation[0].points
                    ],
                    dtype=np.int32,
                )
                mid_x = 0
                mid_y = 0
                if my_lane==annotation[1]:
                    for i in range(len(contours)):
                        mid_x += contours[i][0]
                        mid_y += contours[i][1]

                    mid_x=mid_x/len(contours)
                    mid_y=mid_y/len(contours)

                # Draw detected area
                overlay = cv2.drawContours(
                    image=ret_img.copy(),
                    contours=[contours],
                    contourIdx=-1,
                    color=base_color[num_annotations],
                    thickness=cv2.FILLED,
                )
                result_without_border = cv2.addWeighted(overlay, alpha_shape, ret_img, 1 - alpha_shape, 0)
                ret_img = cv2.drawContours(
                    image=result_without_border,
                    contours=[contours],
                    contourIdx=-1,
                    color=base_color[num_annotations],
                    thickness=2,
                    lineType=cv2.LINE_AA,
                )
                if annotation[1]=="1st" and my_lane=="1st":
                    cv2.circle(ret_img,(int(mid_x),int(mid_y)),5,(255,0,0),-1)
                else:
                    cv2.circle(ret_img,(int(mid_x),int(mid_y)),5,(255,255,0),-1)
                #import pdb; pdb.set_trace()
                Line1_pt=(int(mid_x),int(mid_y))
                if(mid_y > height*0.25):
                    if(mid_x!=0 or mid_y!=0):
                        cv2.arrowedLine(ret_img, btm_pt, mid_pt,(0,255,255),3) ##노란색: 기준선
                        cv2.arrowedLine(ret_img, btm_pt, Line1_pt, (0, 0, 255), 3)
                        #import pdb; pdb.set_trace()
                        ##거리 계산
                        dist1 = cal_dist(btm_pt, mid_pt)
                        dist2 = cal_dist(btm_pt, Line1_pt)
                        dist3 = cal_dist(mid_pt, Line1_pt)
                        ##각도 계산
                        theta = cal_theta(dist1,dist2,dist3)
                        ##
                        vect1 = get_vector(btm_pt, mid_pt)
                        vect2 = get_vector(Line1_pt, mid_pt)
                        ##외적값이 양수일때 양의 각도, 음수일때 음의 각도
                        if Line1_pt[0]<=mid_pt[0]:
                            pass
                        else:
                            theta = -theta
                        theta="{:.2f}".format(theta)
                        
            num_annotations += 1
            if(num_annotations==2):
                break
        if cv2.waitKey(1) & 0xff ==ord('q'):
            break
        cv2.imshow("ret_img", ret_img)
    cap.release()
    cv2.destroyAllWindows()

print("Input your current Lane: ")
my_lane = input()
thread1 = threading.Thread(target=thread_function_server)
thread2 = threading.Thread(target=thread_function_model)

thread1.start()
thread2.start()

# Load image
thread1.join()
thread2.join()

