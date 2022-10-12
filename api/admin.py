from django.contrib import admin
from .models import Movie, Rating

# Register your models here.
admin.site.register(Rating)
admin.site.register(Movie)
