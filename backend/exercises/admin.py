from django.contrib import admin
from .models import Exercise, Pet, Purchases, Owner, Owns, Food

admin.site.register(Exercise),
admin.site.register(Pet),
admin.site.register(Purchases),
admin.site.register(Owner),
admin.site.register(Owns),
admin.site.register(Food)
