from django.shortcuts import render
from django.http import HttpResponse


from django.shortcuts import render, redirect
from .models import MyUser,todouser
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if MyUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Existed  credentials'}, status=401)
        else:
            MyUser.objects.create(username=username, password=password)
            return JsonResponse({'status': 'success', 'message': 'Login successful'}, status=200)
            
    return render(request, 'signup.html')

@csrf_exempt
def send(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        userdata = request.POST.get('userdata')
        days = request.POST.get('days')
        assignments = request.POST.get('assignments')

        print("Received userid:", userid)
        print("Received userdata:", userdata)   


        if not userid or not userdata or not days or not assignments:
            return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

        todouser.objects.create(userid=userid, userdata=userdata,days=days, assignments=assignments)
        return JsonResponse({'status': 'success', 'message': 'Task saved successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = MyUser.objects.filter(username=username, password=password).first()
        
        if user:
            return JsonResponse({'status': 'success', 'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def home2(request):
    return HttpResponse("Hello World 2")




