# send_vid.py
from flask import Response
import cv2

class Send_vid:
    def gen_frames(self):
        self.cap = cv2.VideoCapture(0)
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    def get_response(self):
        return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

