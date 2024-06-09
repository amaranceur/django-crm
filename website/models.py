from django.db import models

# Create your models here.
class Record(models.Model):
    created_at=models.DateTimeField( auto_now_add=True)
    first_name=models.CharField( max_length=50)
    last_name=models.CharField( max_length=50)
    email=models.CharField( max_length=150)
    number=models.CharField( max_length=150)
    address=models.CharField( max_length=50)
    city=models.CharField( max_length=50)
    state=models.CharField( max_length=50)
    zipcode=models.CharField( max_length=50)
    def __str__(self):
        return (self.first_name)