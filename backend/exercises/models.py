from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    solution = models.TextField()
    difficulty = models.CharField(max_length=10)

    def __str__(self):
        return self.title
    
class Pet(models.Model):
    petid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    streetnumber = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    typeofpet = models.CharField(max_length=50)

    class Meta:
        db_table = 'pets'