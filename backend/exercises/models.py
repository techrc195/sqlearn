from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    solution = models.TextField()
    difficulty = models.CharField(max_length=10)

    def __str__(self):
        return self.title
    
class Owner(models.Model):
    OID = models.AutoField(primary_key=True)  
    LastName = models.CharField(max_length=50)
    StreetNumber = models.CharField(max_length=50) # Changed to match schema
    City = models.CharField(max_length=50)
    ZipCode = models.CharField(max_length=10)
    State = models.CharField(max_length=2)
    Age = models.IntegerField() 
    AnnualIncome = models.DecimalField(max_digits=10, decimal_places=2)

class Pet(models.Model):
    PetID = models.AutoField(primary_key=True) # Changed from 'petid'
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    streetnumber = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    typeofpet = models.CharField(max_length=50)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)  # Foreign key added
    liked_foods = models.ManyToManyField('Food', related_name='liked_by') 

class Food(models.Model):
    FoodID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Brand = models.CharField(max_length=50)
    TypeofFood = models.CharField(max_length=20)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    ItemWeight = models.DecimalField(max_digits=10, decimal_places=2)
    ClassofFood = models.CharField(max_length=20)

class Owns(models.Model):
    PetID = models.ForeignKey(Pet, on_delete=models.CASCADE) 
    Year = models.IntegerField()
    OID = models.ForeignKey(Owner, on_delete=models.CASCADE)
    PetAgeatOwnership = models.IntegerField()
    PricePaid = models.DecimalField(max_digits=10, decimal_places=2)

class Purchases(models.Model):
    OID = models.ForeignKey(Owner, on_delete=models.CASCADE)
    FoodID = models.ForeignKey(Food, on_delete=models.CASCADE)
    PetID = models.ForeignKey(Pet, on_delete=models.CASCADE)
    Month = models.IntegerField()
    Year = models.IntegerField()
    Quantity = models.IntegerField() 