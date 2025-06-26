from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.conf import settings
import boto3
from django.shortcuts import render, redirect
from .models import kisandata, MyUser, todouser, daysandassignments, arduinodata, assignmentsuserdata, dbnOrder, dbnOrderItem,SportsDailyActivity,SportsDailyActivityImages,SportsNotificationToken
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import UserDataSerializer, DisplayDataSerializer, ArduinoDataSerializer,SportsDailyActivitySerializer,SportsDailyActivityImageSerializer,SportsNotificationTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import boto3
from django.conf import settings
from django.db.models import Q  # ✅ THIS FIXES YOUR ERROR
from firebase_admin import messaging
from firstapp2.firebase_config import *  # This will initialize Firebase Admin SDK


@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if MyUser.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Existed  credentials'
                },
                status=401)
        else:
            MyUser.objects.create(username=username, password=password)
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Login successful'
                },
                status=200)

    return render(request, 'signup.html')


@csrf_exempt
def assignments_signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        mobilenumber = request.POST['mobilenumber']
        user = request.POST['user']
        college_role = request.POST['college_role']
        feild_key = request.POST['feild_key']
        address = request.POST['address']
        password = request.POST['password']
        if assignmentsuserdata.objects.filter(username=username).exists():
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Existed  credentials'
                },
                status=401)
        else:
            assignmentsuserdata.objects.create(username=username,
                                               mobilenumber=mobilenumber,
                                               user=user,
                                               college_role=college_role,
                                               feild_key=feild_key,
                                               address=address,
                                               password=password)
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Signup successful'
                },
                status=200)

    return JsonResponse(
        {
            'status': 'error',
            'message': 'get request Now allowed'
        }, status=401)


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
            return JsonResponse({
                'status': 'error',
                'message': 'Missing data'
            },
                                status=400)

        todouser.objects.create(userid=userid,
                                userdata=userdata,
                                days=days,
                                assignments=assignments)
        return JsonResponse({
            'status': 'success',
            'message': 'Task saved successfully'
        })

    return JsonResponse(
        {
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405)


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
            return JsonResponse({
                'status': 'success',
                'result': result,
                'time': time
            })
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

        user = MyUser.objects.filter(username=username,
                                     password=password).first()

        if user:
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Login successful'
                },
                status=200)
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid credentials'
                },
                status=401)

    return JsonResponse(
        {
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405)


@csrf_exempt
def assignments_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = assignmentsuserdata.objects.filter(username=username,
                                                  password=password).first()

        if user:
            if user.approval:  # Check if approval is True
                return JsonResponse(
                    {
                        'status': 'success',
                        'message': 'Login successful'
                    },
                    status=200)
            else:
                return JsonResponse(
                    {
                        'status': 'pending',
                        'message': 'Please wait for admin approval.'
                    },
                    status=403)
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Invalid credentials'
                },
                status=401)

    return JsonResponse(
        {
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405)


@csrf_exempt
def get_assignments(request):
    if request.method == 'POST':
        days = request.POST.get('days')
        assignments = request.POST.get('assignments')
        description = request.POST.get('description')

        print("Received days:", days)
        print("Received assignments:", assignments)
        print("Received decsription:", description)

        if not days or not assignments or not description:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing data'
            },
                                status=400)

        daysandassignments.objects.create(days=days,
                                          assignments=assignments,
                                          description=description)
        return JsonResponse({
            'status': 'success',
            'message': 'Task saved successfully'
        })

    return JsonResponse(
        {
            'status': 'error',
            'message': 'Invalid request method'
        }, status=405)


class upload_file_to_s3(APIView):

    def post(self, request, format=None):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({"error": "No file provided"},
                            status=status.HTTP_400_BAD_REQUEST)

        s3 = boto3.client('s3',
                          region_name='ap-south-1',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        s3.upload_fileobj(file_obj, settings.AWS_STORAGE_BUCKET_NAME,
                          file_obj.name)

        file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{file_obj.name}"
        return Response({"url": file_url}, status=status.HTTP_200_OK)


class receive_files_from_s3(APIView):

    def get(self, request):
        s3 = boto3.client('s3',
                          region_name='ap-south-1',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        try:
            response = s3.list_objects_v2(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            files = []
            for item in response.get('Contents', []):
                files.append(
                    f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{s3.meta.region_name}.amazonaws.com/{item['Key']}"
                )

            return Response({"files": files})
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllUsers(APIView):

    def get(self, request):
        users = assignmentsuserdata.objects.all()
        data = [{
            "id": user.id,
            "username": user.username,
            "approval": user.approval
        } for user in users]
        return Response(data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserApproval(APIView):

    def post(self, request):
        try:
            body = json.loads(request.body)
            username = body.get('username')
            approval = body.get('approval')

            if username is None or approval is None:
                return Response({"error": "Missing username or approval"},
                                status=400)

            try:
                user = assignmentsuserdata.objects.get(username=username)
                user.approval = approval
                user.save()
                return Response({"message": "Approval status updated"},
                                status=200)
            except assignmentsuserdata.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


@csrf_exempt
def dbn_place_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            address = data.get('address')
            items = data.get('items', [])

            order = dbnOrder.objects.create(username=username, address=address)

            for item in items:
                product_info = item.split(" - ")
                dbnOrderItem.objects.create(
                    order=order,
                    product_name=product_info[0],
                    option=product_info[1] if len(product_info) > 1 else "")

            return JsonResponse({'message': 'Order placed successfully'},
                                status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def dbn_get_order(request):
    if request.method == 'GET':
        orders = dbnOrder.objects.all().order_by('-created_at')
        data = []
        for order in orders:
            items = [
                f"{item.product_name} - {item.option}"
                for item in order.items.all()
            ]
            data.append({
                "username": order.username,
                "address": order.address,
                "items": items
            })
        return JsonResponse(data, safe=False)


def home2(request):
    return HttpResponse("Hello World 2")


@csrf_exempt
def kisan_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        user_type = data.get('user_type')  # "Farmer" or "Buyer"
        full_name = data.get('full_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')

        # Optional fields for farmers
        no_of_acres = data.get('no_of_acres')
        crop_type = data.get('crop_type')
        has_equipment = data.get('has_equipment') == 'Yes'
        pricing_per_hour = data.get('pricing_per_hour')
        pricing_per_day = data.get('pricing_per_day')
        pricing_per_week = data.get('pricing_per_week')
        pricing_per_month = data.get('pricing_per_month')
        pricing_per_acre = data.get('pricing_per_acre')
        location = data.get('location')
        language = data.get('language')

        user = kisandata.objects.create(user_type=user_type,
                                        full_name=full_name,
                                        email=email,
                                        phone_number=phone_number,
                                        password=password,
                                        no_of_acres=no_of_acres,
                                        crop_type=crop_type,
                                        has_equipment=has_equipment,
                                        pricing_per_hour=pricing_per_hour,
                                        pricing_per_day=pricing_per_day,
                                        pricing_per_week=pricing_per_week,
                                        pricing_per_month=pricing_per_month,
                                        pricing_per_acre=pricing_per_acre,
                                        location=location,
                                        language=language)
        return JsonResponse({'message': 'User registered successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def kisan_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        identifier = data.get('identifier')  # email or phone
        password = data.get('password')

        try:
            user = kisandata.objects.get(Q(email=identifier)
                                         | Q(phone_number=identifier),
                                         password=password)

            return JsonResponse({
                'message': 'Login successful',
                'user_type': user.user_type,
                'full_name': user.full_name,
                'email': user.email,
                'phone_number': user.phone_number
            })
        except kisandata.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


class postSportsDailyActivityView(APIView):
    def post(self, request, format=None):
        # Create the Activity
        serializer = SportsDailyActivitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        activity = serializer.save()

        # Upload images to AWS S3
        s3 = boto3.client('s3',
                          region_name='ap-south-1',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        folder_name = "sportsactivityimages"

        for key in request.FILES:
            file_obj = request.FILES[key]
            filename = f"{folder_name}/{activity.activity_type}_{file_obj.name}"  # save to subfolder
            s3.upload_fileobj(file_obj, settings.AWS_STORAGE_BUCKET_NAME, filename)

            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.ap-south-1.amazonaws.com/{filename}"

            SportsDailyActivityImages.objects.create(activity=activity, image_url=file_url)

        return Response(SportsDailyActivitySerializer(activity).data, status=status.HTTP_201_CREATED)




class getSportsDailyActivityView(APIView):
    def get(self, request, format=None):
        activities = SportsDailyActivity.objects.all().order_by('-date')
        serializer = SportsDailyActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class postSportsNotificationTokenView(APIView):
    def post(self, request):
        serializer = SportsNotificationTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            token = serializer.validated_data['device_token']

            # Optional: update if user already has a token
            obj, created = SportsNotificationToken.objects.update_or_create(
                username=username,
                defaults={'device_token': token}
            )

            return Response({'message': 'Token saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class getSportsNotificationTokenView(APIView):
    def get(self, request):
        tokens = SportsNotificationToken.objects.values_list('device_token', flat=True)
        return Response({'tokens': list(tokens)})
class SendSportsActivityNotificationToAll(APIView):
    def post(self, request):
        title = request.data.get("title")
        body = request.data.get("body")

        tokens = list(SportsNotificationToken.objects.values_list("device_token", flat=True))

        if not tokens:
            return Response({"message": "No tokens to send."}, status=200)

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            tokens=tokens,
        )

        response = messaging.send_multicast(message)

        return Response({
            "sent": response.success_count,
            "failed": response.failure_count,
        }, status=200)




