from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import logging
import asyncio
logger = logging.getLogger(__name__)


class NotificationConsumer(WebsocketConsumer):
    
    def connect(self):
        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.group_name = str(self.scope["user"].pk)  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

    def disconnect(self, close_code):
        self.close()

    def notify(self, event):
        notification = {
            'message': "this is the message",
            'data': "this is the data"
        }
        self.send(text_data=json.dumps(notification))
        

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "users_group"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_initial_data()

    async def send_initial_data(self):
        users = await self.fetch_users()
        await self.send(text_data=json.dumps({'users': users}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info("WebSocket disconnected.")

    async def receive(self, text_data):
        logger.info("Received data from client: %s", text_data)
        await self.user_change()

    async def user_change(self, event=None):
        logger.info("Received user change event.")
        try:
            logger.info("Fetching User Data.")
            users = await self.fetch_users()
            await self.send(text_data=json.dumps({'users': users}))
            
        except Exception as e:
            logger.error("Error fetching users: %s", e)
            
    async def user_delete(self, event=None):
        logger.info("Received user delete event.")
        try:
            logger.info("Fetching User Data.")
            users = await self.fetch_users()
            await self.send(text_data=json.dumps({'users': users}))
            
        except Exception as e:
            logger.error("Error fetching users: %s", e)
            
            
    @database_sync_to_async
    def fetch_users(self):
        from invent_app.models import CustomUser 
        asyncio.run(asyncio.sleep(1))        
        users = CustomUser.objects.all().values('id', 'username', 'first_name', 'last_name', 'email', 'last_login')
        users_list = []
        for user in users:
            user['last_login'] = user['last_login'].isoformat() if user['last_login'] else None
            users_list.append(user)
        return users_list