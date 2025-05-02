import json
from pprint import pprint
from django.shortcuts import get_object_or_404
from a_rtchat.models import ChatGroup, GroupMessage
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name'] 
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        
        # add and update online users
        # if self.user not in self.chatroom.users_online.all():
        #     self.chatroom.users_online.add(self.user)
        #     self.update_online_count()
        print("===================connect===================")
        
        
        self.accept()
        
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )
        print("===================disconnect===================")
        
        # remove and update online users
        # if self.user in self.chatroom.users_online.all():
        #     self.chatroom.users_online.remove(self.user)
        #     self.update_online_count() 
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        message = GroupMessage.objects.create(
            body = body,
            author = self.user, 
            group = self.chatroom 
        )
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        
        print("===================received===================")
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
        
    def message_handler(self, event):
        
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        is_author = message.author == self.user
        context = {
            'message': message,
            'user': self.user,
            'chat_group': self.chatroom,
            'is_author': is_author,
        }
        print("===================handler===================")
        
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)
    