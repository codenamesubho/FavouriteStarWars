from django.urls import include, path
from rest_framework import routers
from .views import (
    MovieListView,
    PlanetListView,
    FavouriteMovieView,
    FavouritePlanetView,
)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("planets/", PlanetListView.as_view(), name="planet-list"),
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("favourite/movie/", FavouriteMovieView.as_view(), name="favourite-movie"),
    path("favourite/planet/", FavouritePlanetView.as_view(), name="favourite-planet"),
]
