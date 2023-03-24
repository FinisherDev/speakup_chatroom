from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

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
def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password :
            if User.objects.filter(username=username):
                messages.info(request, 'Username already exists.')
                return redirect('register')
            elif User.objects.filter(email = email):
                messages.info(request, 'Email already exists.')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
                user.save()
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
                return redirect ('chatroom')
        else:
            messages.warning(request, 'Your passwords are not the same')
            return redirect('register')
    else:
        return render(request, 'home/signup.html')
