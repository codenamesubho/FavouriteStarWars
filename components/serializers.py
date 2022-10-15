from rest_framework.serializers import ModelSerializer
from .models import Movie, Planet, FavouriteMovie, FavouritePlanet


class MovieListSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "release_date", "created", "updated", "url"]


class PlanetListSerializer(ModelSerializer):
    class Meta:
        model = Planet
        fields = ["id", "name", "created", "updated", "url"]


class FavouriteMovieSerializer(ModelSerializer):
    class Meta:
        model = FavouriteMovie
        fields = ["id", "user_id", "movie", "custom_title"]


class FavouritePlanetSerializer(ModelSerializer):
    class Meta:
        model = FavouritePlanet
        fields = ["id", "user_id", "planet", "custom_name"]
