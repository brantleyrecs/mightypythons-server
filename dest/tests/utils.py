import random

from faker import Faker

from destapi.models import Destination, Activity, DestAct, User, Climate


def create_data(cls):
    cls.faker = Faker()
    cls.users = []
    cls.destinations = []
    cls.activities = []
    cls.climates = []
    cls.destacts = []

    for _ in range(0, 10):
        user = User.objects.create(
            name=cls.faker.name(),
            uid=cls.faker.name()
        )
        cls.users.append(user)

        activity = Activity.objects.create(
            name=cls.faker.name(),
            bio=cls.faker.name()
        )
        cls.activities.append(activity)

        for _ in range(0, 10):
            climate = Climate.objects.create(
                name=cls.faker.name()
            )
            cls.climates.append(climate)
            
            
            destination = Destination.objects.create(
                name=cls.faker.name(),
                bio=cls.faker.sentence(),
                image=cls.faker.url(),
                climate=climate,
                user=user
            )
            cls.destinations.append(destination)

            destact = DestAct.objects.create(
                destination=destination,
                activity=activity,
            )
            cls.destacts.append(destact)


def refresh_data(self):
    for user in self.users:
        user.refresh_from_db()
    for climate in self.climates:
        climate.refresh_from_db()
    for activity in self.activities:
        activity.refresh_from_db()
    for destination in self.destinations:
        destination.refresh_from_db()
    for destact in self.destacts:
        destact.refresh_from_db()
