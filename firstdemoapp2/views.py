from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.conf import settings
import boto3
from django.shortcuts import render, redirect
from .models import MyUser,todouser,daysandassignments,arduinodata
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserDataSerializer,DisplayDataSerializer,ArduinoDataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import boto3
from django.conf import settings


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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_arduino(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = data.get('result')
            time2 = data.get('time')
            time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

            print("✅ Received in Django:", result, time)
            
            
            arduinodata.objects.create(result=result, time=time)
            return JsonResponse({'status': 'success', 'result': result, 'time': time})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Only POST allowed'}, status=405)


@api_view(['GET'])
def get_user_data(request):
    data = todouser.objects.all()
    serializer = UserDataSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_display(request):
    data = daysandassignments.objects.all()
    serializer = DisplayDataSerializer(data, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def receive_arduino(request):
    
    data = arduinodata.objects.all()
    serializer = ArduinoDataSerializer(data, many=True)
    return Response(serializer.data)
    


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

@csrf_exempt
def get_assignments(request):
    if request.method == 'POST':
        days = request.POST.get('days')
        assignments = request.POST.get('assignments')
        description = request.POST.get('description')
        

        print("Received days:", days)
        print("Received assignments:", assignments)   
        print("Received decsription:", description)   



        if not days or not assignments or not description :
            return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

        daysandassignments.objects.create(days=days, assignments=assignments,description=description)
        return JsonResponse({'status': 'success', 'message': 'Task saved successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


class upload_file_to_s3(APIView):
    def post(self, request, format=None):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        s3 = boto3.client(
            's3',
            region_name='ap-south-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        s3.upload_fileobj(file_obj, settings.AWS_STORAGE_BUCKET_NAME, file_obj.name)

        file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{file_obj.name}"
        return Response({"url": file_url}, status=status.HTTP_200_OK)
    
class receive_files_from_s3(APIView):
    def get(self, request):
        s3 = boto3.client(
            's3',
            region_name='ap-south-1',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        try:
            response = s3.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            files = []
            for item in response.get('Contents', []):
                files.append(f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{s3.meta.region_name}.amazonaws.com/{item['Key']}")

            return Response({"files": files})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def home2(request):
    return HttpResponse("Hello World 2")







