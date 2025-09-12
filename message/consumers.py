import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from .serializers import MessageSerializer
from main_app.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.channel_id = self.scope['url_route']['kwargs']['channel_id']
        self.group_name = f'chat_{self.channel_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'message':
            message = await self.save_message(data)
            await self.channel_layer.group_send(
                self.group_name,
                {'type': 'send_message', 'message': message}
            )

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message']
        }))

    @database_sync_to_async
    def save_message(self, data):
        message = Message.objects.create(
            channel_id=self.channel_id,
            sender=self.scope['user'],  # ✅ now CustomUser
            content=data.get('content', ''),
            message_type=data.get('message_type', 'text')
        )
        return MessageSerializer(message).data
