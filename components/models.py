from django.db import models

# Create your models here.


class Planet(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    url = models.URLField()


class Movie(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    release_date = models.DateTimeField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    url = models.URLField()


class FavouritePlanet(models.Model):
    user_id = models.PositiveIntegerField()
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    custom_name = models.CharField(max_length=250, null=True)

    class Meta:
        unique_together = (
            "user_id",
            "planet",
        )


class FavouriteMovie(models.Model):
    user_id = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    custom_title = models.CharField(max_length=250, null=True)

    class Meta:
        unique_together = (
            "user_id",
            "movie",
        )
