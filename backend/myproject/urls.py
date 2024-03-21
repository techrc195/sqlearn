from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exercises/', include('exercises.urls'), name='exercise_list'),
    path('', lambda request: redirect('exercises/', permanent=False)),
]

