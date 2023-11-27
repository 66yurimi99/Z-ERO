import asyncio
import cv2
from socket_server import VideoStreamerServer

async def process_image(image_data):
    # Process the received image data
    cv2.imshow("receive", image_data)
    cv2.waitKey(1)

if __name__ == "__main__":
    server = VideoStreamerServer(5000)
    asyncio.get_event_loop().run_until_complete(server.start_server(process_image))
