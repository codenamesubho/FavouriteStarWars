from django.core.management.base import BaseCommand, CommandError
from components.models import Movie, Planet
from components.utils import fetch_all_records


class Command(BaseCommand):
    """
    Command to fetch data from external api and seed the database
    """

    help = "Populate Database"

    def handle(self, *args, **options):
        Planet.objects.all().delete()
        Movie.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Successfully cleaned database"))
        MOVIE_API_URL = "https://swapi.dev/api/films/"
        PLANET_API_URL = "https://swapi.dev/api/planets/"

        all_movies = fetch_all_records(MOVIE_API_URL)
        all_planets = fetch_all_records(PLANET_API_URL)
        all_movie_objects = []
        all_planet_objects = []

        for node in all_movies:
            title = node.get("title")
            release_date = node.get("release_date")
            created = node.get("created")
            updated = node.get("edited")
            url = node.get("url")
            all_movie_objects.append(
                Movie(
                    title=title,
                    release_date=release_date,
                    created=created,
                    updated=updated,
                    url=url,
                )
            )

        for node in all_planets:
            name = node.get("name")
            created = node.get("created")
            updated = node.get("edited")
            url = node.get("url")
            all_planet_objects.append(
                Planet(name=name, created=created, updated=updated, url=url)
            )

        Movie.objects.bulk_create(all_movie_objects)
        Planet.objects.bulk_create(all_planet_objects)
        self.stdout.write(
            self.style.SUCCESS(
                f"Database populated| Movie records: {len(all_movie_objects)}| Planet records: {len(all_planet_objects)}"
            )
        )
