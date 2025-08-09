from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest
from .models import UserProfile, DataEntry
from .views import create_data_entry, view_data_entries, check_user_role
from django.core.exceptions import PermissionDenied

class ContributorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('contributor', password='pass')
        UserProfile.objects.create(user=self.user, is_manager=False)
        self.manager = User.objects.create_user('manager', password='pass')
        UserProfile.objects.create(user=self.manager, is_manager=True)
        self.request = HttpRequest()
        self.entry = DataEntry.objects.create(content='Test', created_by=self.user)

    def test_create_data(self):
        self.request.user = self.user
        new_entry = create_data_entry(self.request, 'New Content')
        self.assertEqual(new_entry.content, 'New Content')

    def test_view_data(self):
        self.request.user = self.user
        entries = view_data_entries(self.request)
        self.assertTrue(entries.exists())