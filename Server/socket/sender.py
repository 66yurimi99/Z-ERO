import asyncio
import cv2
from socket_client import VideoStreamerClient

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

async def process_image(image_data):
    # Process the received image data
    print("sender")

if __name__ == "__main__":
    

    client = VideoStreamerClient("ws://localhost:5000")
    asyncio.get_event_loop().run_until_complete(client.start_client(cap))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
    
