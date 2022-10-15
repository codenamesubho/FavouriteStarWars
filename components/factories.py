from .models import Movie, Planet, FavouriteMovie, FavouritePlanet

import factory


class MovieFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("name")
    release_date = factory.Faker("date_time")
    created = factory.Faker("date_time")
    updated = factory.Faker("date_time")
    url = factory.Faker("url")

    class Meta:
        model = Movie


class PlanetFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("company")
    created = factory.Faker("date_time")
    updated = factory.Faker("date_time")
    url = factory.Faker("url")

    class Meta:
        model = Planet


class FavouriteMovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavouriteMovie


class FavouritePlanetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavouritePlanet
