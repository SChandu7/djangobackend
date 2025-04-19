from django.shortcuts import render
from django.http import HttpResponse


from django.shortcuts import render, redirect
from .models import MyUser
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if MyUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            MyUser.objects.create(username=username, password=password)
            messages.success(request, 'Account created successfully')
            return redirect('/login/')
    return render(request, 'signup.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = MyUser.objects.filter(username=username, password=password).first()
        if user:
            messages.success(request, 'Account Logined successfully')

            
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def home2(request):
    return HttpResponse("Hello World 2")




