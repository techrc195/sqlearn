from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=255)
    schema_description = models.TextField(blank=True)
    description = models.TextField()
    solution = models.TextField()
    difficulty = models.CharField(max_length=10)

    class Meta:
        db_table = 'exercises'

    def __str__(self):
        return self.title
    
class Owner(models.Model):
    oid = models.AutoField(primary_key=True)  
    lastname = models.CharField(max_length=50)
    streetnumber = models.CharField(max_length=50) 
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    age = models.IntegerField() 
    annualincome = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'owners'

class Food(models.Model):
    foodid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    typeoffood = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    itemweight = models.DecimalField(max_digits=10, decimal_places=2)
    classoffood = models.CharField(max_length=20)

    class Meta:
        db_table = 'foods'

class Pet(models.Model):
    petid = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    streetnumber = models.CharField(max_length=255) # Renamed for consistency
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    typeofpet = models.CharField(max_length=50) 
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, db_column='oid') 
    liked_foods = models.ManyToManyField(Food, through='Likes', related_name='liked_by_pets')

    class Meta:
        db_table = 'pets'

class Owns(models.Model):
    petid = models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='petid') 
    year = models.IntegerField()
    oid = models.ForeignKey(Owner, on_delete=models.CASCADE, db_column='oid')
    petageatownership = models.IntegerField()
    pricepaid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'owns'

class Purchases(models.Model):
    oid = models.ForeignKey(Owner, on_delete=models.CASCADE, db_column='oid')
    foodid = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='foodid')
    petid = models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='petid')
    month = models.IntegerField()
    year = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'purchases' 

class Likes(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='petid')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, db_column='foodid')

    class Meta:
        db_table = 'likes'