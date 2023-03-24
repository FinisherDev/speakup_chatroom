from django.shortcuts import render
from django.contrib.auth.models import User, auth
from chatroom.serializers import MessageSerializer, UserSerializer
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from chatroom.models import Messages
from django.views.decorators.csrf import csrf_exempt
from home.views import index

# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect ('chatroom')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('home')
    else:
        return render(request, 'home/home_page.html')

@csrf_exempt
def user_list(request, pk=None):
    if request.method == "GET":
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request' : request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chatroom/dashboard.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chatroom/messages.html", {'users': User.objects.exclude(username=request.user.username), 'receiver': User.objects.get(id=receiver), 'messages': Messages.objects.filter(sender_id=sender, receiver_id=receiver) | Messages.objects.filter(sender_id=receiver, receiver_id=sender)})
    elif request.method == "POST":
        message = request.POST['message']
        msg_saved = Messages(sender_id=sender, receiver_id=receiver, message=message)
        msg_saved.save()
        return render(request, "chatroom/messages.html", {'users': User.objects.exclude(username=request.user.username), 'receiver': User.objects.get(id=receiver), 'messages': Messages.objects.filter(sender_id=sender, receiver_id=receiver) | Messages.objects.filter(sender_id=receiver, receiver_id=sender)})
