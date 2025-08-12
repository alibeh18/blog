from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import UserProfile, DataEntry, CustomUser
from .views import create_data_entry, view_data_entries
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

class ContributorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('contributor', password='pass')
        UserProfile.objects.create(user=self.user, is_manager=False)
        self.manager = User.objects.create_user('manager', password='pass')
        UserProfile.objects.create(user=self.manager, is_manager=True)
        self.entry = DataEntry.objects.create(content='Test', created_by=self.user)
        self.custom_user = CustomUser.objects.create(username='testuser1', password='mypassword123')
        self.token = 'your_token_here'

    def test_create_data(self):
        request = HttpRequest()
        request.user = self.user
        new_entry = create_data_entry(request, 'New Content')
        self.assertEqual(new_entry.content, 'New Content')

    def test_view_data(self):
        request = HttpRequest()
        request.user = self.user
        entries = view_data_entries(request)
        self.assertTrue(entries.exists())

    def test_create_custom_user_api(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(
            '/contributor/api/create_user/',
            {'username': 'newuser_api', 'password': 'newpass789'},
            format='json'
        )
        self.assertEqual(response.status_code, 201)
        user = CustomUser.objects.get(username='newuser_api')
        self.assertTrue(user.check_password('newpass789'))

    def test_create_custom_user_non_manager(self):
        self.client.credentials()
        response = self.client.post(
            '/contributor/api/create_user/',
            {'username': 'newuser3', 'password': 'pass789'},
            format='json'
        )
        self.assertEqual(response.status_code, 401)

    def test_check_password(self):
        self.assertTrue(self.custom_user.check_password('mypassword123'))
        self.assertFalse(self.custom_user.check_password('wrongpass'))