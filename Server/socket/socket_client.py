import asyncio
import websockets
import base64
import cv2
import numpy as np

class VideoStreamerClient:
    def __init__(self, server_url):
        self.server_url = server_url

    async def send_image(self, websocket, image_data):
        await websocket.send(image_data)

    async def start_client(self, cap):

        async with websockets.connect(self.server_url) as websocket:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                _, buffer = cv2.imencode('.jpg', frame)
                image_data = base64.b64encode(buffer).decode('utf-8')

                await self.send_image(websocket, image_data)

                await asyncio.sleep(0.03)
