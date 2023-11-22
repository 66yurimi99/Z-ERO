import numpy as np
import cv2

def read_cam():
    cap = cv2.VideoCapture("http://192.168.100.146:5000/video_feed")  #(IP address is raspberry pi)
    w = 640  # 1280#1920
    h = 480  # 720#1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
    return cap

def show_cam(cap):
    if not cap.isOpened():
        print("Camera is closed...")
    else:
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret is False:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Display
            cv2.imshow("Camera", frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break

if __name__=='__main__':
    cap = read_cam()
    show_cam(cap)
    cap.release()
    cv2.destroyAllWindows()