from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FavouriteMovie, FavouritePlanet

from .serializers import (
    MovieListSerializer,
    PlanetListSerializer,
    FavouriteMovieSerializer,
    FavouritePlanetSerializer,
)

from .models import Planet, Movie


class MovieListView(APIView):
    def get(self, request):
        """
        Api to get list of movies,
        if user_id is provided, we fetch movies and overwrite titles from user favourites
        if title is provided, we filter movies based on title and from user favourites
        """
        title = request.query_params.get("title")
        user_id = request.query_params.get("user_id")

        queryset = Movie.objects.all()

        if user_id:
            user_favourites = FavouriteMovie.objects.filter(user_id=user_id)
        else:
            user_favourites = FavouriteMovie.objects.none()

        if title:
            user_favourites = user_favourites.filter(custom_title=title)
            favourite_renamed_movies = [obj.movie_id for obj in user_favourites]
            queryset = queryset.filter(
                Q(title=title) | Q(id__in=favourite_renamed_movies)
            ).distinct()

        user_favourites_map = {
            obj.movie_id: obj.custom_title for obj in user_favourites
        }
        movie_data = MovieListSerializer(queryset, many=True).data
        for node in movie_data:
            if node["id"] in user_favourites_map:
                custom_title = user_favourites_map[node["id"]]
                if custom_title:
                    node["title"] = custom_title
                node["is_favourite"] = True
            else:
                node["is_favourite"] = False

        return Response({"results": movie_data})


class PlanetListView(APIView):
    def get(self, request):
        """
        Api to get list of planets,
        if user_id is provided, we fetch planets and overwrite name from user favourites
        if name is provided, we filter planets based on name and from user favourites
        """
        name = request.query_params.get("name")
        user_id = request.query_params.get("user_id")

        queryset = Planet.objects.all()

        if user_id:
            user_favourites = FavouritePlanet.objects.filter(user_id=user_id)
        else:
            user_favourites = FavouritePlanet.objects.none()

        if name:
            user_favourites = user_favourites.filter(custom_name=name)
            favourite_renamed_planets = [obj.planet_id for obj in user_favourites]
            queryset = queryset.filter(
                Q(name=name) | Q(id__in=favourite_renamed_planets)
            ).distinct()

        user_favourites_map = {
            obj.planet_id: obj.custom_name for obj in user_favourites
        }
        planet_data = PlanetListSerializer(queryset, many=True).data
        for node in planet_data:
            if node["id"] in user_favourites_map:
                custom_name = user_favourites_map[node["id"]]
                if custom_name:
                    node["name"] = custom_name
                node["is_favourite"] = True
            else:
                node["is_favourite"] = False

        return Response({"results": planet_data})


class FavouriteMovieView(APIView):
    def post(self, request):
        """
        Api to add movie to user favourite
        """
        serializer = FavouriteMovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class FavouritePlanetView(APIView):
    def post(self, request):
        """
        Api to add planet to user favourite
        """
        serializer = FavouritePlanetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
