from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from components.models import Movie, Planet, FavouriteMovie, FavouritePlanet
from django.utils import timezone
from components.serializers import PlanetListSerializer, FavouritePlanetSerializer
import json
from components.factories import (
    MovieFactory,
    PlanetFactory,
    FavouriteMovieFactory,
    FavouritePlanetFactory,
)
from faker import Faker

faker = Faker()


class PlanetListApiTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        PlanetFactory.create_batch(2)
        super().setUpClass()

    def test_get_planetlist_without_any_param(self):
        """
        Get List of planet when no params are sent
        """
        url = reverse("planet-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = PlanetListSerializer(Planet.objects.all(), many=True).data
        for node in data:
            node["is_favourite"] = False
        output = json.loads(json.dumps({"results": data}))
        self.assertEqual(response.json(), output)

    def test_get_planetlist_with_user_param(self):
        """
        Get List of planet when user param is sent and no user favourite exist
        """
        url = reverse("planet-list")
        response = self.client.get(url, data={"user_id": 10}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = PlanetListSerializer(Planet.objects.all(), many=True).data
        for node in data:
            node["is_favourite"] = False
        output = json.loads(json.dumps({"results": data}))
        self.assertEqual(response.json(), output)

    def test_get_planetlist_with_name_param(self):
        """
        Get List of planet when name is sent and no favourites exist, validate api returns only matching object
        """
        url = reverse("planet-list")
        planet = Planet.objects.first()
        response = self.client.get(url, data={"name": planet.name}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = PlanetListSerializer(Planet.objects.get(name=planet.name)).data
        data["is_favourite"] = False
        output = json.loads(json.dumps({"results": [data]}))
        self.assertEqual(response.json(), output)

    def test_get_planetlist_with_user_param_and_favourite(self):
        """
        Validate when user is passed and favourites exist, planet name are overwritten as per user defined in favourites
        """
        planet_with_custom_name = PlanetFactory()
        planet_without_custom_name = PlanetFactory()

        custom_name_1 = faker.word()
        user_id_1 = faker.pyint()
        FavouritePlanetFactory(
            planet=planet_with_custom_name,
            user_id=user_id_1,
            custom_name=custom_name_1,
        )

        custom_name_2 = faker.word()
        user_id_2 = faker.pyint(min_value=user_id_1 + 1)

        FavouritePlanetFactory(
            planet=planet_with_custom_name,
            user_id=user_id_2,
            custom_name=custom_name_2,
        )
        FavouritePlanetFactory(planet=planet_without_custom_name, user_id=user_id_2)

        # validate user_2 sees planet name as set in favourites custom_name
        # incase where its in favourite but no custom name is provided, it retains its original name
        url = reverse("planet-list")
        response = self.client.get(url, data={"user_id": user_id_2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), Planet.objects.count())
        for node in response.json()["results"]:
            if planet_with_custom_name.id == node["id"]:
                self.assertEqual(node["name"], custom_name_2)
                self.assertNotEqual(node["name"], planet_with_custom_name.name)
                self.assertTrue(node["is_favourite"])
            elif planet_without_custom_name.id == node["id"]:
                self.assertEqual(node["name"], planet_without_custom_name.name)
                self.assertTrue(node["is_favourite"])
            else:
                self.assertFalse(node["is_favourite"])

        # validate user_1 sees its own custom_name
        url = reverse("planet-list")
        response = self.client.get(url, data={"user_id": user_id_1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), Planet.objects.count())
        for node in response.json()["results"]:
            if planet_with_custom_name.id == node["id"]:
                self.assertEqual(node["name"], custom_name_1)
                self.assertNotEqual(node["name"], planet_with_custom_name.name)
                self.assertTrue(node["is_favourite"])
            else:
                self.assertFalse(node["is_favourite"])

    def test_get_planetlist_with_user_and_title_param_and_favourite(self):
        """
        Validate when user and search name is passed and favourites exist, planets are searched based on name as well as names
        defined in favourites
        """
        search_name_1 = faker.word()
        planet_with_custom_name = PlanetFactory()
        planet_without_custom_name = PlanetFactory(name=search_name_1)

        user_id_1 = faker.pyint()
        FavouritePlanetFactory(
            planet=planet_with_custom_name,
            user_id=user_id_1,
            custom_name=search_name_1,
        )

        search_name_2 = faker.word()
        custom_name_2 = f"{search_name_2}{faker.word()}"
        user_id_2 = faker.pyint(min_value=user_id_1 + 1)

        FavouritePlanetFactory(
            planet=planet_with_custom_name,
            user_id=user_id_2,
            custom_name=custom_name_2,
        )
        FavouritePlanetFactory(planet=planet_without_custom_name, user_id=user_id_2)

        # validate user_1 sees 2 records one matches name and another matches favorites custom name
        url = reverse("planet-list")
        response = self.client.get(
            url, data={"user_id": user_id_1, "name": search_name_1}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 2)
        for node in response.json()["results"]:
            if planet_with_custom_name.id == node["id"]:
                self.assertEqual(node["name"], search_name_1)
                self.assertNotEqual(node["name"], planet_with_custom_name.name)
                self.assertTrue(node["is_favourite"])
            elif planet_without_custom_name.id == node["id"]:
                self.assertEqual(node["name"], search_name_1)
                self.assertEqual(node["name"], planet_without_custom_name.name)
                self.assertFalse(node["is_favourite"])

        # Incase of user 2, searched name partially matches with only favourite custom name, hence 1 record returned
        url = reverse("planet-list")
        response = self.client.get(
            url, data={"user_id": user_id_2, "name": search_name_2}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)
        for node in response.json()["results"]:
            if planet_with_custom_name.id == node["id"]:
                self.assertEqual(node["name"], custom_name_2)
                self.assertNotEqual(node["name"], planet_with_custom_name.name)
                self.assertTrue(node["is_favourite"])


class FavouritePlanetApiTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        PlanetFactory.create_batch(2)
        super().setUpClass()

    def test_post_add_favourite_planet(self):
        """
        Validating Api call to add planet to user favourite
        """
        planet = Planet.objects.first()
        user_id = faker.pyint()
        url = reverse("favourite-planet")
        response = self.client.post(
            url, data={"planet": planet.id, "user_id": user_id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = FavouritePlanetSerializer(FavouritePlanet.objects.first()).data
        self.assertEqual(response.json(), {"data": data})

    def test_post_add_favourite_planet_with_custom_name(self):
        """
        Validating Api call to add planet to user favourite with custom_name
        """
        planet = Planet.objects.first()
        user_id = faker.pyint()
        url = reverse("favourite-planet")
        custom_name = faker.word()
        response = self.client.post(
            url,
            data={"planet": planet.id, "user_id": user_id, "custom_name": custom_name},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = FavouritePlanetSerializer(FavouritePlanet.objects.first()).data
        self.assertEqual(response.json(), {"data": data})

    def test_post_add_favourite_planet_with_incorrect_param(self):
        """
        Validating favourite Api , returns validationerror incase the parameters are malformed
        """
        # invalid planet_id
        user_id = faker.pyint()
        url = reverse("favourite-planet")
        custom_name = faker.word()
        response = self.client.post(
            url,
            data={
                "planet": faker.pyint(),
                "user_id": user_id,
                "custom_name": custom_name,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # invalid user_id
        planet = Planet.objects.first()
        response = self.client.post(
            url,
            data={
                "planet": planet.id,
                "user_id": faker.word(),
                "custom_name": custom_name,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
