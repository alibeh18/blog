from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest
from contributor_app.models import UserProfile, DataEntry
from .views import create_data_entry, edit_data_entry, delete_data_entry, view_data_entries
from django.core.exceptions import PermissionDenied

class ManagerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('contributor', password='pass')
        UserProfile.objects.create(user=self.user, is_manager=False)
        self.manager = User.objects.create_user('manager', password='pass')
        UserProfile.objects.create(user=self.manager, is_manager=True)
        self.request = HttpRequest()
        self.entry = DataEntry.objects.create(content='Test', created_by=self.user)

    def test_create_data(self):
        self.request.user = self.manager
        new_entry = create_data_entry(self.request, 'Manager Content')
        self.assertEqual(new_entry.content, 'Manager Content')

    def test_edit_data_manager(self):
        self.request.user = self.manager
        edited = edit_data_entry(self.request, self.entry.id, 'Edited')
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.content, 'Edited')

    def test_edit_data_contributor_fail(self):
        self.request.user = self.user
        with self.assertRaises(PermissionDenied):
            edit_data_entry(self.request, self.entry.id, 'Try')

    def test_delete_data_manager(self):
        self.request.user = self.manager
        delete_data_entry(self.request, self.entry.id)
        self.assertFalse(DataEntry.objects.filter(id=self.entry.id).exists())

    def test_delete_data_contributor_fail(self):
        self.request.user = self.user
        with self.assertRaises(PermissionDenied):
            delete_data_entry(self.request, self.entry.id)

    def test_view_data(self):
        self.request.user = self.manager
        entries = view_data_entries(self.request)
        self.assertTrue(entries.exists())