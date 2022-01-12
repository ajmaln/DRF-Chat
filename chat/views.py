from datetime import time
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message, UserProfile
from chat.serializers import MessageSerializer, UserSerializer


def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')


@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            UserProfile.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)

## Rasa part start 


# importing the requests library
import requests
  
# api-endpoint
URL = "http://10.100.14.175:5001/webhooks/rest/webhook"

def call_rasa(data):

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
            "sender": data["sender"],
            "message": data["message"]
        }
    # sending get request and saving the response as response object
    r = requests.post(url = URL, json = PARAMS)
    print("*"*100, '\n')
    print(type(r.text), r.text)
    bot_result =  eval(r.text)
    print(bot_result, type(bot_result))
    # r = [{"recipient_id":"test","text":"Can you please type your account number?"}]
    for item in bot_result:
        print(item)
        bot_data = {
            "sender": "rasa-bot",
            "receiver": item["recipient_id"],
            "message": item["text"],
            "timestamp": "1234454"
        }
        user_id = int(User.objects.get(username=item["recipient_id"]).pk)
        requests.post(url = f'http://10.100.14.175:8100/api/messages/4/{user_id}',\
                json=bot_data)

  

## rasa end



@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            # data = {'sender': 'ridwan', 'receiver': 'rasa-bot', 'message': 'HELLO'}
            serializer = MessageSerializer(data=data) 
            
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        finally:
            if data["receiver"] == 'rasa-bot':
                call_rasa(data)
        return JsonResponse(serializer.errors, status=400)


def register_view(request):
    """
    Render registration template
    """
    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'chat/register.html', {})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver,agent = 6):
    if not request.user.is_authenticated:
        return redirect('index')
    
    messages = Message.objects.filter(sender_id=sender, receiver_id=receiver) |Message.objects.filter(sender_id=receiver, receiver_id=sender)

    if sender == 9:
        agent_messages = Message.objects.filter(sender_id=9, receiver_id=6) |Message.objects.filter(sender_id=6, receiver_id=9)
        messages = agent_messages | messages
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': messages})



# unit test 
# from chat.models import Message
# x = Message.objects.filter(sender_id=9, receiver_id=6) |Message.objects.filter(sender_id=6, receiver_id=9)
# for item in x:
# ...     print(item.sender_id)
# 

# >>> messages = Message.objects.filter(sender_id=9, receiver_id=4) |Message.objects.filter(sender_id=4, receiver_id=6)                     
# >>> agent_messages = Message.objects.filter(sender_id=9, receiver_id=6) |Message.objects.filter(sender_id=6, receiver_id=9)
## total_messages = agent_messages | messages