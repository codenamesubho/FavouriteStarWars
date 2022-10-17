from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from components.models import Movie, Planet, FavouriteMovie, FavouritePlanet
from django.utils import timezone
from components.serializers import (
    MovieListSerializer,
    PlanetListSerializer,
    FavouriteMovieSerializer,
)
import json
from components.factories import (
    MovieFactory,
    PlanetFactory,
    FavouriteMovieFactory,
    FavouritePlanetFactory,
)
from faker import Faker

faker = Faker()


class MovieListApiTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        MovieFactory.create_batch(2)
        super().setUpClass()

    def test_get_movielist_without_any_param(self):
        """
        Get List of movies when no params are sent
        """
        url = reverse("movie-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = MovieListSerializer(Movie.objects.all(), many=True).data
        for node in data:
            node["is_favourite"] = False
        output = json.loads(json.dumps({"results": data}))
        self.assertEqual(response.json(), output)

    def test_get_movielist_with_user_param(self):
        """
        Get List of movies when user param is sent but no favourite movie is added
        """
        url = reverse("movie-list")
        response = self.client.get(url, data={"user_id": 10}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = MovieListSerializer(Movie.objects.all(), many=True).data
        for node in data:
            node["is_favourite"] = False
        output = json.loads(json.dumps({"results": data}))
        self.assertEqual(response.json(), output)

    def test_get_movielist_with_title_param(self):
        """
        Get List of movies when title is sent and no favourites exist, validate api returns only matching object
        """
        url = reverse("movie-list")
        movie = Movie.objects.first()
        response = self.client.get(url, data={"title": movie.title}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = MovieListSerializer(Movie.objects.get(title=movie.title)).data
        data["is_favourite"] = False
        output = json.loads(json.dumps({"results": [data]}))
        self.assertEqual(response.json(), output)

    def test_get_movielist_with_user_param_and_favourite(self):
        """
        Validate when user is passed and favourites exist, movie titles are overwritten as per user defined in favourites
        """
        movie_with_custom_title = MovieFactory()
        movie_without_custom_title = MovieFactory()

        custom_title_1 = faker.word()
        user_id_1 = faker.pyint()
        FavouriteMovieFactory(
            movie=movie_with_custom_title,
            user_id=user_id_1,
            custom_title=custom_title_1,
        )

        custom_title_2 = faker.word()
        user_id_2 = faker.pyint(min_value=user_id_1 + 1)

        FavouriteMovieFactory(
            movie=movie_with_custom_title,
            user_id=user_id_2,
            custom_title=custom_title_2,
        )
        FavouriteMovieFactory(movie=movie_without_custom_title, user_id=user_id_2)

        # validate user_2 sees title as set in favourites custom_title
        # incase where its in favourite but no custom title is provided, it retains its original title
        url = reverse("movie-list")
        response = self.client.get(url, data={"user_id": user_id_2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), Movie.objects.count())
        for node in response.json()["results"]:
            if movie_with_custom_title.id == node["id"]:
                self.assertEqual(node["title"], custom_title_2)
                self.assertNotEqual(node["title"], movie_with_custom_title.title)
                self.assertTrue(node["is_favourite"])
            elif movie_without_custom_title.id == node["id"]:
                self.assertEqual(node["title"], movie_without_custom_title.title)
                self.assertTrue(node["is_favourite"])
            else:
                self.assertFalse(node["is_favourite"])

        # validate user_1 sees its own custom_title
        url = reverse("movie-list")
        response = self.client.get(url, data={"user_id": user_id_1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), Movie.objects.count())
        for node in response.json()["results"]:
            if movie_with_custom_title.id == node["id"]:
                self.assertEqual(node["title"], custom_title_1)
                self.assertNotEqual(node["title"], movie_with_custom_title.title)
                self.assertTrue(node["is_favourite"])
            else:
                self.assertFalse(node["is_favourite"])

    def test_get_movielist_with_user_and_title_param_and_favourite(self):
        """
        Validate when user and search title is passed and favourites exist, movies are searched based on title as well as titles
        defined in favourites
        """
        search_title_1 = faker.word()
        movie_with_custom_title = MovieFactory()
        movie_without_custom_title = MovieFactory(title=search_title_1)

        user_id_1 = faker.pyint()
        FavouriteMovieFactory(
            movie=movie_with_custom_title,
            user_id=user_id_1,
            custom_title=search_title_1,
        )

        search_title_2 = faker.word()
        custom_title_2 = f"{search_title_2}{faker.word()}"
        user_id_2 = faker.pyint(min_value=user_id_1 + 1)

        FavouriteMovieFactory(
            movie=movie_with_custom_title,
            user_id=user_id_2,
            custom_title=custom_title_2,
        )
        FavouriteMovieFactory(movie=movie_without_custom_title, user_id=user_id_2)

        # validate user_1 sees 2 records one matches title and another matches favorites custom title
        url = reverse("movie-list")
        response = self.client.get(
            url, data={"user_id": user_id_1, "title": search_title_1}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 2)
        for node in response.json()["results"]:
            if movie_with_custom_title.id == node["id"]:
                self.assertEqual(node["title"], search_title_1)
                self.assertNotEqual(node["title"], movie_with_custom_title.title)
                self.assertTrue(node["is_favourite"])
            elif movie_without_custom_title.id == node["id"]:
                self.assertEqual(node["title"], search_title_1)
                self.assertEqual(node["title"], movie_without_custom_title.title)
                self.assertFalse(node["is_favourite"])

        # Incase of user 2, searched title partially matches with only favourite custom title, hence 1 record returned
        url = reverse("movie-list")
        response = self.client.get(
            url, data={"user_id": user_id_2, "title": search_title_2}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)
        for node in response.json()["results"]:
            if movie_with_custom_title.id == node["id"]:
                self.assertEqual(node["title"], custom_title_2)
                self.assertNotEqual(node["title"], movie_with_custom_title.title)
                self.assertTrue(node["is_favourite"])


class FavouriteMovieApiTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        MovieFactory.create_batch(2)
        super().setUpClass()

    def test_post_add_favourite_movie(self):
        """
        Validating Api call to add movie to user favourite
        """
        movie = Movie.objects.first()
        user_id = faker.pyint()
        url = reverse("favourite-movie")
        response = self.client.post(
            url, data={"movie": movie.id, "user_id": user_id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = FavouriteMovieSerializer(FavouriteMovie.objects.first()).data
        self.assertEqual(response.json(), {"data": data})

    def test_post_add_favourite_movie_with_custom_title(self):
        """
        Validating Api call to add movie to user favourite with custom_title
        """
        movie = Movie.objects.first()
        user_id = faker.pyint()
        url = reverse("favourite-movie")
        custom_title = faker.word()

        response = self.client.post(
            url,
            data={"movie": movie.id, "user_id": user_id, "custom_title": custom_title},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = FavouriteMovieSerializer(FavouriteMovie.objects.first()).data
        self.assertEqual(response.json(), {"data": data})

    def test_post_add_favourite_movie_with_incorrect_param(self):
        """
        Validating favourite Api , returns validationerror incase the parameters are malformed
        """

        # invalid movie_id
        user_id = faker.pyint()
        url = reverse("favourite-movie")
        custom_title = faker.word()
        response = self.client.post(
            url,
            data={
                "movie": faker.pyint(),
                "user_id": user_id,
                "custom_title": custom_title,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # invalid user_id
        movie = Movie.objects.first()
        response = self.client.post(
            url,
            data={
                "movie": movie.id,
                "user_id": faker.word(),
                "custom_title": custom_title,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
