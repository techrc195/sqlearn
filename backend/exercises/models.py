from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    solution = models.TextField()
    difficulty = models.CharField(max_length=10)

    class Meta:
        db_table = 'exercises'

    def __str__(self):
        return self.title
    
class Owner(models.Model):
    OID = models.AutoField(primary_key=True)  
    LastName = models.CharField(max_length=50)
    StreetNumber = models.CharField(max_length=50) 
    City = models.CharField(max_length=50)
    ZipCode = models.CharField(max_length=10)
    State = models.CharField(max_length=2)
    Age = models.IntegerField() 
    AnnualIncome = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'owners'

class Food(models.Model):
    FoodID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Brand = models.CharField(max_length=50)
    TypeofFood = models.CharField(max_length=20)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    ItemWeight = models.DecimalField(max_digits=10, decimal_places=2)
    ClassofFood = models.CharField(max_length=20)

    class Meta:
        db_table = 'foods'

class Pet(models.Model):
    PetID = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    StreetNumber = models.CharField(max_length=255) # Renamed for consistency
    City = models.CharField(max_length=50)
    ZipCode = models.CharField(max_length=10)
    State = models.CharField(max_length=2)
    typeofpet = models.CharField(max_length=50) 
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, db_column='oid') 
    liked_foods = models.ManyToManyField(Food, through='Likes', related_name='liked_by_pets')

    class Meta:
        db_table = 'pets'

class Owns(models.Model):
    PetID = models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='petid') 
    Year = models.IntegerField()
    OID = models.ForeignKey(Owner, on_delete=models.CASCADE, db_column='oid')
    PetAgeatOwnership = models.IntegerField()
    PricePaid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'owns'

class Purchases(models.Model):
    OID = models.ForeignKey(Owner, on_delete=models.CASCADE, db_column='oid')
    FoodID = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='foodid')
    PetID = models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='petid')
    Month = models.IntegerField()
    Year = models.IntegerField()
    Quantity = models.IntegerField()

    class Meta:
        db_table = 'purchases' 

class Likes(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='petid')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='foodid')

    class Meta:
        db_table = 'likes'