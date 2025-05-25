from django.db import models

class MyUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
class todouser(models.Model):
    userid = models.CharField(max_length=100)
    userdata = models.CharField(max_length=100)
    days = models.CharField(max_length=100,default='')
    assignments = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.userid


