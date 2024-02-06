from rest_framework import status
from rest_framework.test import APITestCase

from destapi.models import Climate

from .utils import create_data, refresh_data


class TestClimates(APITestCase):

    @classmethod
    def setUpTestData(cls):
        create_data(cls)

    def setUp(self):
        refresh_data(self)

    def test_create(self):
        new_climate= {
            "name": self.faker.name()
        }
        response = self.client.post("/climates", new_climate)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data

        self.assertTrue("id" in data)
        self.assertTrue("name" in data)

        db_climate = Climate.objects.get(pk=data["id"])
        self.assertEqual(db_climate.name, new_climate["name"])

    def test_delete(self):
        climate_id = Climate.objects.all()[0].id
        response = self.client.delete(f"/climates/{climate_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse("data" in response)

        climate = Climate.objects.filter(id=climate_id)
        self.assertEqual(len(climate), 0)

    def test_update(self):
        climate_id = Climate.objects.all()[0].id
        updated_climate = {
            "name": self.faker.sentence(nb_words=3)
        }
        response = self.client.put(
            f"/climates/{climate_id}", updated_climate, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)

        db_climate = Climate.objects.get(pk=climate_id)
        self.assertEqual(db_climate.name, updated_climate["name"])

    def test_list(self):
        response = self.client.get("/climates")
        data = response.data

        self.assertEqual(len(data), len(self.climates))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_climate = data[0]
        self.assertTrue("id" in first_climate)
        self.assertTrue("name" in first_climate)

    def test_details(self):
        climate = Climate.objects.all()[0]
        response = self.client.get(f"/climates/{climate.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["id"], climate.id)
        self.assertEqual(data["name"], climate.name)
