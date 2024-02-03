from rest_framework import status
from rest_framework.test import APITestCase

from destapi.models import Destination

from .utils import create_data, refresh_data


class TestDestinations(APITestCase):

    @classmethod
    def setUpTestData(cls):
        create_data(cls)

    def setUp(self):
        refresh_data(self)

    def test_create(self):
        climate = self.climates[0]
        user = self.users[0]
        new_destination= {
            "name": self.faker.name(),
            "bio": self.faker.sentence(),
            "image": self.faker.url(),
            "climate_id": climate.id,
            "user_id": user.id
        }
        response = self.client.post("/destinations", new_destination)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data

        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("bio" in data)
        self.assertTrue("image" in data)
        self.assertTrue("climate_id" in data)
        self.assertTrue("user_id" in data)


        db_destination = Destination.objects.get(pk=data["id"])
        self.assertEqual(db_destination.name, new_destination["name"])

    def test_delete(self):
        destination_id = Destination.objects.all()[0].id
        response = self.client.delete(f"/destinations/{destination_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse("data" in response)

        destination = Destination.objects.filter(id=destination_id)
        self.assertEqual(len(destination), 0)

    def test_update(self):
        climate = self.climates[0]
        user = self.users[0]
        destination_id = Destination.objects.all()[0].id
        updated_destination = {
            "name": self.faker.sentence(nb_words=3),
            "bio": self.faker.sentence(),
            "image": self.faker.url(),
            "climate_id": climate.id,
            "user_id": user.id
        }
        response = self.client.put(
            f"/destinations/{destination_id}", updated_destination, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("bio" in data) 
        self.assertTrue("image" in data)
        self.assertTrue("climate_id" in data)
        self.assertTrue("user_id" in data)

        db_destination = Destination.objects.get(pk=destination_id)
        self.assertEqual(db_destination.name, updated_destination["name"])

    def test_list(self):
        response = self.client.get("/destinations")
        data = response.data

        self.assertEqual(len(data), len(self.destinations))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_destination = data[0]
        self.assertTrue("id" in first_destination)
        self.assertTrue("name" in first_destination)
        self.assertTrue("bio" in first_destination)
        self.assertTrue("image" in first_destination)
        self.assertTrue("climate_id" in first_destination)
        self.assertTrue("user_id" in first_destination)

    def test_details(self):
        destination = Destination.objects.all()[0]
        response = self.client.get(f"/destinations/{destination.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["id"], destination.id)
        self.assertEqual(data["name"], destination.name)
        self.assertEqual(data["bio"], destination.bio)
        self.assertEqual(data["image"], destination.image)
        self.assertEqual(data["climate_id"], destination.climate)
        self.assertEqual(data["user_id"], destination.user)
