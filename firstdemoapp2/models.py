from django.db import models


class MyUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class assignmentsuserdata(models.Model):
    username = models.CharField(max_length=100, unique=True)
    mobilenumber = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    college_role = models.CharField(max_length=100)
    feild_key = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    approval = models.BooleanField(default=False)


class todouser(models.Model):
    userid = models.CharField(max_length=100)
    userdata = models.CharField(max_length=50000)
    days = models.CharField(max_length=100, default='')
    assignments = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.userid


class daysandassignments(models.Model):
    days = models.CharField(max_length=100)
    assignments = models.CharField(max_length=50000)
    description = models.CharField(max_length=5000, default='')

    def __str__(self):
        return self.days


class arduinodata(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=100)


class dbnOrder(models.Model):
    username = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class dbnOrderItem(models.Model):
    order = models.ForeignKey(dbnOrder,
                              related_name='items',
                              on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    option = models.CharField(max_length=100)


class kisandata(models.Model):
    USER_TYPE_CHOICES = (
        ('Farmer', 'Farmer'),
        ('Buyer', 'Buyer'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    # Only for Farmers
    no_of_acres = models.CharField(max_length=20, blank=True, null=True)
    crop_type = models.CharField(max_length=100, blank=True, null=True)
    has_equipment = models.BooleanField(default=False)
    pricing_per_hour = models.CharField(max_length=20, blank=True, null=True)
    pricing_per_day = models.CharField(max_length=20, blank=True, null=True)
    pricing_per_week = models.CharField(max_length=20, blank=True, null=True)
    pricing_per_month = models.CharField(max_length=20, blank=True, null=True)
    pricing_per_acre = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.user_type})"


    
class SportsDailyActivity(models.Model):
    pt_name = models.CharField(max_length=100)
    activity_type = models.CharField(max_length=100)
    game_name = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=50)
    school = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class SportsDailyActivityImages(models.Model):
    activity = models.ForeignKey(SportsDailyActivity, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()



