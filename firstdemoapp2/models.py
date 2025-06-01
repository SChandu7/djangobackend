from django.db import models

class MyUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


    def __str__(self):
        return self.username
class todouser(models.Model):
    userid = models.CharField(max_length=100)
    userdata = models.CharField(max_length=5000)
    days = models.CharField(max_length=1000,default='')
    assignments = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.userid
class daysandassignments(models.Model):
    days = models.CharField(max_length=100)
    assignments = models.CharField(max_length=100)
    description = models.CharField(max_length=100,default='')
    

    def __str__(self):
        return self.userid
    
class arduinodata(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=100)


