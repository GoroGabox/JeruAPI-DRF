from channels.generic.websocket import AsyncWebsocketConsumer
import json


class PedidoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('pedidos', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Logic for when a connection is closed
        pass

    async def receive(self, text_data):
        # Logic for when data is received
        data = json.loads(text_data)
        if data.get('message') == 'ping':
            await self.send(text_data=json.dumps({"message": "pong"}))

    async def send_message(self, action, data):
        # Logic for sending messages to the channel
        await self.send(text_data=json.dumps({"action": action, "data": data}))

    async def send_pedido_update(self, event):
        action = event["action"]
        data = event["data"]
        await self.send(text_data=json.dumps({
            "type": "pedido_update",
            "action": action,
            "pedido": data
        }))
