# streamapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        frame_data = text_data_json["data"]  # This is your base64 encoded image

        # For testing, let's just print a confirmation that a frame was received
        print("Frame received")