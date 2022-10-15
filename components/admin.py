from django.contrib import admin

from .models import FavouritePlanet, FavouriteMovie, Movie, Planet

# Register your models here.

admin.site.register(Planet)
admin.site.register(Movie)
admin.site.register(FavouriteMovie)
admin.site.register(FavouritePlanet)
