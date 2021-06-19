from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import Message
from .serializers import MessageSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.http import Http404
from rest_framework import viewsets
from rest_framework.authtoken.models import Token 
from rest_framework.decorators import api_view, permission_classes

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication

def index(request):
    return render(request, 'index.html')

def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')
    messages = Message.objects.filter(room=room_name)[0:25]

    return render(request, 'room.html', {'room_name': room_name, 'username': username, 'messages': messages})

class WebToken(TokenAuthentication):
    keyword = "Bearer"    


class GetView(APIView):
    serializer_class = MessageSerializer
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippet = Message.objects.all()
        serializer = MessageSerializer(snippet,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = MessageSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'ok':'Succesfully created'},status=status.HTTP_200_OK)
        return Response({'Error':'Failed Succesfully'},status=status.HTTP_400_BAD_REQUEST)    

class GetNewMessageView(APIView):
    serializer_class = MessageSerializer
    authentication_classes = [WebToken]

    def get_object(self, pk):
        try:
            return Message.objects.get(receiver=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        snippet = Message.objects.filter(receiver = request.user).filter(room = pk).filter(msgread = False)
        serializer = MessageSerializer(snippet,many=True)
        return Response(serializer.data)
    


@api_view(['GET'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({"error":"Please add user,password"},status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username = username,password=password)
    if not user:
        return Response({"error":"Invalid Credentials"},status=status.HTTP_404_NOT_FOUND)
    
    token,_ = Token.objects.get_or_create(user=user)
    return Response({"token":token.key},status=status.HTTP_200_OK)
    

