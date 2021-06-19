import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message
from channels.db import database_sync_to_async
from django.contrib.auth.models import User,AnonymousUser

import urllib.parse as urlparse
from urllib import parse

import datetime
import pytz 

from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        user = self.scope['user']
        print(self.room_name)
        print("status User",user)
        await self.update_user_status(user,"online")
        
        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.seen_zone_msg(user,self.room_name)
        

    
    async def disconnect(self, close_code):
        
        user = self.scope['user']
        await self.update_user_status(user,"offline")
        
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print("From Web Socket:" , data)
        message = data['message']
        username = data['username']
        room = data['room']
        receiver = data['receiver']
        receivertype = data['receivertype']

        await self.save_message(username, room, message,receiver,receivertype)
        await self.update_msgread(username,receiver)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'receiver':receiver,
                'receivertype':receivertype
                
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        print("From Receive Group:", message)
        receiver = event['receiver']
        receivertype = event['receivertype']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'receiver':receiver,
            'receivertype':receivertype
        }))

    @sync_to_async
    def save_message(self, username, room, message,receiver,receivertype):
        print("Inside Save")
        Message.objects.create(username=username, room=room, content=message,receiver = receiver,receivertype = receivertype)

    @database_sync_to_async
    def update_user_status(self, user, statususer):
        """
        Updates the user `status.
        `status` can be one of the following status: 'online', 'offline' or 'away'
        """
        print("inside Update",user,statususer)
        check = Message.objects.filter(username=user)
        if check is not None:
            for i in range(0,len(check)):
                check[i].status = statususer
                check[i].save()
            print("Saved Updated completed")
        else:
            print("Null User :",user)

    @database_sync_to_async
    def update_msgread(self,user,receiverend):
        print("Inside Msg Read")
        #Checking all messages is there or not
        message = Message.objects.filter(receiver=receiverend).filter(username = user)
        print(message)
        #If messages are there then perform msgRead operation
        if message is not None:
            #get receiver end status whethere offline or online
            getreceiverstatus = Message.objects.filter(username=receiverend).first()
            if getreceiverstatus is  not None:
                print(getreceiverstatus.username)
                print(getreceiverstatus.status)
                print(getreceiverstatus.last_seen)
                now = datetime.datetime.now() #current live time now
                gettingnotreadmsg = Message.objects.filter(date_added__range =(getreceiverstatus.last_seen,now))
                print("-----Getting Not read Msgs-------")
                print(gettingnotreadmsg)

                #if receiverstatus is ONLINE ,then update msgs or sender and receiver as TRUE or else False
                if getreceiverstatus.status == 'online':
                    for i in range(0,len(message)):
                        message[i].msgread = True
                        message[i].save()
                        print("Msg Status :", message[i].msgread)
                else:
                    #Need to validate based on time of last_seen  
                    for i in range(0,len(gettingnotreadmsg)):
                        gettingnotreadmsg[i].msgread = False
                        gettingnotreadmsg[i].save()
                        print("Msg Status :", gettingnotreadmsg[i].msgread)
            else:
                print("Not found receiver status")
        else:
            print("Not Found")

    @database_sync_to_async
    def seen_zone_msg(self,user,roomname):
        print("Current User at Seen Zone is ", user)
        print("Current User at seen zone Room is :",roomname)

        getuser = Message.objects.filter(receiver = user,room = roomname)
        if  getuser.count() !=  0:
            for i in range(0,len(getuser)):
                getuser[i].msgread = True
                getuser[i].save()
                print("Msg Status :", getuser[i].msgread)
            print(getuser)
        else:
            print("Null at Current User Get")