import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MerchantOrdersConsumer(AsyncWebsocketConsumer):
    group_name = 'merchants'

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Basic heartbeat/ping support
        try:
            data = json.loads(text_data or '{}') if text_data else {}
        except Exception:
            data = {}
        if data.get('type') == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))

    async def order_event(self, event):
        # event: { 'type': 'order.event', 'order': {...} }
        payload = {k: v for k, v in event.items() if k != 'type'}
        await self.send(text_data=json.dumps(payload))
