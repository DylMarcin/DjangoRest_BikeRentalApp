from django.db import models
from datetime import datetime, timedelta


# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=50)
    tel = models.CharField(max_length=50)
    personal_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.CharField(max_length=50)

    def __str__(self):
         return "{}, {}".format(self.name, self.personal_number)

class Bike(models.Model):
    bike_id_number = models.CharField(max_length=50)
    producer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    created = models.DateField(default=datetime.now().date())
    available = models.BooleanField(default=True)

    def __str__(self):
        return "{} {} - {}".format(self.producer, self.model, self.bike_id_number)

class Rental(models.Model):
    client = models.ForeignKey(Client, related_name='client', on_delete=models.CASCADE)
    bike_id_number = models.ManyToManyField(Bike) # Foreign key
    created = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.client.name, self.created)
