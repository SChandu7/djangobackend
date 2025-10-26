# ⚙️ Django REST API Backend — Sports & Event Management System

A powerful **Django REST API backend** designed for managing and retrieving sports and event data.  
It supports **secure CRUD operations**, **API-based data access**, and **MySQL database integration**, fully hosted on **AWS EC2** for scalability and accessibility.  

This backend serves as the core for multiple applications — including **Flutter frontends, web dashboards**, and **AI-based analytics systems**.

---

## 🚀 Features

- 🧠 **Django REST Framework (DRF)** powered API backend  
- 📦 **MySQL database** integration for structured storage  
- 🔐 Secure **token-based API access**  
- 📨 Support for **POST** (insert), **GET** (fetch), **PUT/PATCH** (update), and **DELETE** operations  
- ☁️ **Deployed on AWS EC2** for public API usage  
- ⚙️ **CORS enabled** for frontend integration (Flutter / React)  
- 📄 Well-documented models and serializers for easy customization  

---

## 🧩 Tech Stack

| Component | Technology Used |
|------------|-----------------|
| **Framework** | Django 5.x |
| **API Toolkit** | Django REST Framework (DRF) |
| **Database** | MySQL |
| **Server** | AWS EC2 (Ubuntu) |
| **Web Server** | Gunicorn + Nginx |
| **Environment** | Python 3.10+ |
| **Frontend** | Flutter / React (optional) |

---

## 🧠 API Overview

### 🔹 Base URL

[https://My-Django-endpoint/api/](http://13.203.219.206:8000/)

pgsql
Copy code

### 🔹 Example Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/events/` | Retrieve all event records |
| `GET` | `/events/<id>/` | Retrieve specific event data |
| `POST` | `/events/` | Add a new event result |
| `PUT` | `/events/<id>/` | Update existing event |
| `DELETE` | `/events/<id>/` | Delete an event |
| `GET` | `/participants/` | List all participants |
| `POST` | `/participants/` | Add new participant |

---

## 🧱 Models Structure

Example: `models.py`

```python
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=[
        ('Intramural', 'Intramural'),
        ('Extramural', 'Extramural'),
        ('State', 'State'),
        ('National', 'National'),
    ])
    date = models.DateField()
    venue = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name} - {self.level}"

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=[
        ('Winner', 'Winner'),
        ('Runner', 'Runner'),
        ('Participant', 'Participant')
    ])

    def __str__(self):
        return f"{self.name} ({self.team})"

```

## 🧩 Serializers
Example: serializers.py

```

from rest_framework import serializers
from .models import Event, Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

```
## 🔁 How Serializers Work
- Convert model instances → JSON for API responses.
- Parse incoming JSON → Python objects for POST/PUT.
- Ensure data validation and field mapping between DB and API.

## ⚙️ Views (API Logic)
Example: views.py

```

from rest_framework import viewsets
from .models import Event, Participant
from .serializers import EventSerializer, ParticipantSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

```

## 🌐 URLs
python
```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ParticipantViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```
---
# 🧰 Local Setup (Development)
## 1️⃣ Clone Repository
bash
```
git clone https://github.com/SChandu7/djangobackend.git
cd djangobackend
```
## 2️⃣ Create Virtual Environment
bash
```
python -m venv env
source env/bin/activate  # (Windows: env\Scripts\activate)
```
## 3️⃣ Install Dependencies
bash
```
pip install -r requirements.txt
```

## 4️⃣ Configure Database
Edit settings.py:

python
```

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sportsdb',
        'USER': 'admin',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 5️⃣ Migrate Database
bash
```
python manage.py makemigrations
python manage.py migrate
```
## 6️⃣ Run Locally
bash
```
python manage.py runserver
```
---

## ☁️ AWS EC2 Deployment
- Step 1: Launch EC2 Instance
Choose Ubuntu 22.04

Allow inbound rules for ports 22, 80, and 8000

- Step 2: Connect to EC2
bash
```
ssh -i "your-key.pem" ubuntu@<your-ec2-ip>
```
- Step 3: Install Dependencies
bash
```
sudo apt update
sudo apt install python3-pip python3-venv nginx mysql-server
```
- Step 4: Clone Project
bash
```
git clone https://github.com/SChandu7/djangobackend.git
cd djangbackend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
- Step 5: Setup Gunicorn & Nginx
bash
```
gunicorn --bind 0.0.0.0:8000 djangobackend.wsgi:application
sudo systemctl start nginx
```
- Step 6: Configure Nginx Proxy
Add to /etc/nginx/sites-available/default:

nginx
```
location / {
    proxy_pass http://127.0.0.1:8000;
}
```
Then restart:

bash
```
sudo systemctl restart nginx
```
- ✅ Your Django REST API is now accessible globally via:

perl
```
http://<your-ec2-public-ip>/api/
```

---

## 🧠 API Testing
Test using:

Postman / cURL

Example:

bash
```
curl -X GET http://<your-ec2-ip>/api/events/
curl -X POST http://<your-ec2-ip>/api/events/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Football","category":"Sports","level":"Intramural","date":"2025-01-25","venue":"Main Ground"}'
```
## 🧾 Example Response
json
```
{
  "id": 1,
  "name": "Football",
  "category": "Sports",
  "level": "Intramural",
  "date": "2025-01-25",
  "venue": "Main Ground",
  "participants": [
    {
      "id": 1,
      "name": "Team A",
      "team": "Dept of AI",
      "position": "Winner"
    }
  ]
}
```
 ---
 
## 💡 Benefits
- ✅ Reusable, modular backend
- ✅ Public APIs for any frontend (Flutter, React, Web)
 - ✅ Secure & scalable on AWS
- ✅ Structured data for analytics and AI usage
 - ✅ Can be expanded with authentication and file uploads

- 🧭 Future Improvements
- 🔐 JWT Authentication

- 📸 Image upload for event results

- 📊 Analytics endpoints

- 🌍 Multi-user role access (admin, student, committee)

- 📈 Excel/CSV export APIs

--- 

## 🧑‍💻 Developer Info
Author: S. Chandu

Project: Sports Data Management Backend

Framework: Django REST API

Database: MySQL

Host: AWS EC2

Frontend Integration: Almost 20+ Applications

---
## 🏆 License
This project is licensed under the MIT License.
You’re free to use, modify, and distribute for academic and research purposes.

---


## Contact

If you have any questions or suggestions regarding the Coffee app, feel free to contact us at kingchandus143@gmail.com 

---
