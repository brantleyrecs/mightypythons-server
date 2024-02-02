from rest_framework import status
from rest_framework.test import APITestCase

from destapi.models import Activity

from .utils import create_data, refresh_data


class TestActivites(APITestCase):

    @classmethod
    def setUpTestData(cls):
        create_data(cls)

    def setUp(self):
        refresh_data(self)

    def test_create(self):
        new_activity= {
            "name": self.faker.name(),
            "bio": self.faker.sentence()
        }
        response = self.client.post("/activites", new_activity)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.data

        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("bio" in data)

        db_activity = Activity.objects.get(pk=data["id"])
        self.assertEqual(db_activity.name, new_activity["name"])

    def test_delete(self):
        activity_id = Activity.objects.all()[0].id
        response = self.client.delete(f"/activites/{activity_id}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse("data" in response)

        activity = Activity.objects.filter(id=activity_id)
        self.assertEqual(len(activity), 0)

    def test_update(self):
        activity_id = Activity.objects.all()[0].id
        updated_activity = {
            "name": self.faker.sentence(nb_words=3),
            "bio": self.faker.sentence()
        }
        response = self.client.put(
            f"/activites/{activity_id}", updated_activity, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertTrue("id" in data)
        self.assertTrue("name" in data)
        self.assertTrue("bio" in data) 

        db_activity = Activity.objects.get(pk=activity_id)
        self.assertEqual(db_activity.name, updated_activity["name"])

    def test_list(self):
        response = self.client.get("/activites")
        data = response.data

        self.assertEqual(len(data), len(self.activities))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        first_activity = data[0]
        self.assertTrue("id" in first_activity)
        self.assertTrue("name" in first_activity)
        self.assertTrue("bio" in first_activity)

    def test_details(self):
        activity = Activity.objects.all()[0]
        response = self.client.get(f"/activites/{activity.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data

        self.assertEqual(data["id"], activity.id)
        self.assertEqual(data["name"], activity.name)
        self.assertEqual(data["bio"], activity.bio)
