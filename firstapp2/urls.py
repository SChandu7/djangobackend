"""
URL configuration for firstapp2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home, demo, demo2, nothing, yash, navya
from firstdemoapp2.views import signup_view, login_view, home2, send, get_user_data, get_assignments, get_display, send_arduino, receive_arduino, upload_file_to_s3, receive_files_from_s3, assignments_signup_view, assignments_login_view, GetAllUsers, UpdateUserApproval, dbn_place_order, dbn_get_order, kisan_register, kisan_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home/', home2),
    path('demo/', demo),
    path('yash/', yash),
    path('demo/demo/', demo2),
    path('nothing/', nothing),
    path('signup/', signup_view, name='signup'),
    path('assignmentssignup/',
         assignments_signup_view,
         name='assignmentssignup'),
    path('login/', login_view, name='login'),
    path('assignmentslogin/', assignments_login_view, name='assignmentslogin'),
    path('send/', send, name='send'),
    path('navya/', navya, name='navya'),
    path('receive/', get_user_data, name='get_user_data'),
    path('rec/', get_user_data, name='get_user_data'),
    path('assignments/', get_assignments, name='get_assignments'),
    path('display/', get_display, name='get_display'),
    path('arduinosend/', send_arduino, name='send_arduino'),
    path('receive_arduino/', receive_arduino),
    path('uploadfiletos3/', upload_file_to_s3.as_view(), name='file-upload'),
    path('receivefilesfroms3/', receive_files_from_s3.as_view()),
    path('getallusers/', GetAllUsers.as_view(), name='get-all-users'),
    path('updateapproval/',
         UpdateUserApproval.as_view(),
         name='update-user-approval'),
    path('dbnplaceorder/', dbn_place_order, name='dbn_place_order'),
    path('dbngetorder/', dbn_get_order, name='dbn_get_order'),
    path('kisanregister/', kisan_register, name='kisan_register'),
    path('kisanlogin/', kisan_login, name='kisan_login'),
]
