from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestAnnouncements(APITestCase):
    def test_get_announcements(self):
        url = reverse('get-announcements')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSchedule(APITestCase):
    def test_get_schedule(self):
        url = reverse('get-schedule')
        data = {
            'day': 1,
            'group': 32
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
