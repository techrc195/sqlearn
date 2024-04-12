import os
import django
from dotenv import load_dotenv 
from datetime import date
import random
from faker import Faker
import psycopg2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup() 
from exercises.models import Food, Pet, Owner, Owns, Purchases, Likes



load_dotenv() 

# Construct connection parameters using environment variables
conn_params = {
    'host': os.getenv('HOST'), 
    'database': os.getenv('DATABASE'),  
    'user': os.getenv('USER'),  
    'password': os.getenv('PASSWORD') 
}

fake = Faker() 

def generate_owners():
    num_owners = 300
    generated_oids = [] 

    for _ in range(num_owners):
        last_name = fake.last_name()
        street = fake.street_address()
        city = fake.city()
        zipcode = fake.zipcode()
        state = fake.state_abbr()
        age = fake.random_int(min=18, max=80)  
        income = fake.random_int(min=18000, max=80000)  # Generate base income as an integer
        income += round(fake.random.uniform(2, 50), 2)   

        owner = Owner(
            LastName=last_name,
            StreetNumber=street, 
            City=city,
            ZipCode=zipcode,
            State=state,
            Age=age,
            AnnualIncome=income
        )
        owner.save()
        generated_oids.append(owner.OID)  

    return generated_oids 

def generate_foods():
    num_foods = 300
    generated_foodids = []

    for _ in range(num_foods):
        typeoffood = random.choice(['dog', 'cat', 'bird', 'fish'])  # Intended consumer

        # Specific food item based on 'typeoffood'
        if typeoffood == 'dog':
            name = random.choice(['Bone', 'Kibble', 'Treats', 'Chew Stick'])
        elif typeoffood == 'cat':
            name = random.choice(['Tuna', 'Salmon', 'Chicken', 'Soft Food'])
        elif typeoffood == 'bird':
            name = random.choice(['Seed Mix', 'Millet', 'Pellets'])
        elif typeoffood == 'fish':
            name = random.choice(['Flakes', 'Pellets', 'Shrimp'])

        # Other attributes
        brand = fake.company()
        price = round(fake.random.uniform(5, 100), 2)
        weight = round(fake.random.uniform(0.5, 25), 2)
        classoffood = random.choice(['dry food', 'wet food', 'treats'])

        food = Food(
            Name=name,
            Brand=brand,
            TypeofFood=typeoffood,
            Price=price,
            ItemWeight=weight,
            ClassofFood=classoffood
        )
        food.save()
        generated_foodids.append(food.FoodID)

    return generated_foodids

def generate_pets(all_owner_ids):
    num_pets = 300
    generated_petids = []

    for _ in range(num_pets):
        name = fake.first_name_nonbinary()
        age = fake.random_int(min=1, max=15)
        street_number = fake.street_address()  # Field name adjusted
        city = fake.city()
        zipcode = fake.zipcode()
        state = fake.state_abbr()
        typeofpet = random.choice(['dog', 'cat', 'bird', 'fish', 'hamster'])
        owner = Owner.objects.get(OID=random.choice(all_owner_ids)) 

        pet = Pet(
            name=name,
            age=age,
            StreetNumber=street_number,  # Field name adjusted
            City=city,
            ZipCode=zipcode,
            State=state,
            typeofpet=typeofpet,
            owner=owner 
        )
        pet.save()
        generated_petids.append(pet.PetID) 

    return generated_petids

def generate_owns(all_pet_ids, all_owner_ids):
    num_owns = random.randint(300, 500)

    for _ in range(num_owns):
        pet = Pet.objects.get(PetID=random.choice(all_pet_ids))
        owner = Owner.objects.get(OID=random.choice(all_owner_ids))
        year = fake.year()
        age_at_ownership = fake.random_int(min=0, max=14)  
        price_paid = 0 if age_at_ownership > 0 else round(fake.random_number(digits=2), 2)

        owns = Owns(
            PetID=pet,
            Year=year,
            OID=owner,
            PetAgeatOwnership=age_at_ownership,
            PricePaid=price_paid
        )
        owns.save()
 
def generate_likes(all_pet_ids, all_food_ids):
    for pet_id in all_pet_ids:
        pet = Pet.objects.get(PetID=pet_id)
        num_likes = random.randint(1, 3) 
        liked_food_ids = random.sample(all_food_ids, num_likes)

        for food_id in liked_food_ids:
            food = Food.objects.get(FoodID=food_id)  
            like = Likes(pet=pet, food=food) # Create the Likes object
            like.save() 

def generate_purchases(all_pet_ids, all_owner_ids, all_food_ids):
    num_months = 12 
    current_year = date.today().year
    current_month = date.today().month

    for _ in range(random.randint(300, 600)): 
        pet = Pet.objects.get(PetID=random.choice(all_pet_ids))
        owner = Owner.objects.get(OID=random.choice(all_owner_ids))
        food = Food.objects.get(FoodID=random.choice(all_food_ids))
        quantity = random.randint(1, 3) 
        
        year = current_year if random.random() < 0.8 else current_year - 1 
        month = random.randint(1, current_month) if year == current_year else random.randint(1, 12)

        purchase = Purchases(
            OID=owner,
            FoodID=food,
            PetID=pet,
            Month=month,
            Year=year,
            Quantity=quantity
        )
        purchase.save()
 
# Main Execution
if __name__ == '__main__':
    all_owner_ids = generate_owners()
    all_food_ids = generate_foods() 
    all_pet_ids = generate_pets(all_owner_ids) 

    generate_owns(all_pet_ids, all_owner_ids)
    generate_likes(all_pet_ids, all_food_ids)
    generate_purchases(all_pet_ids, all_owner_ids, all_food_ids)