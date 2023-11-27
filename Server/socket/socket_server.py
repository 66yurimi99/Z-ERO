import websockets
import base64
import cv2
import numpy as np


class VideoStreamerServer:
    def __init__(self, port):
        self.port = port

    async def receive_image(self, websocket):
        image_data = await websocket.recv()
        buffer = base64.b64decode(image_data)
        nparr = np.frombuffer(buffer, dtype=np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return image

    async def start_server(self, callback):
        async def handler(websocket, path):
            while True:
                image_data = await self.receive_image(websocket)
                await callback(image_data)

        server = await websockets.serve(handler, "localhost", self.port)
        await server.wait_closed()
