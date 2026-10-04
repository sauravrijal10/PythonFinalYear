import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase


class EnsureSuperuserCommandTests(TestCase):
	@patch.dict(
		os.environ,
		{
			"DJANGO_SUPERUSER_EMAIL": "admin@example.com",
			"DJANGO_SUPERUSER_PASSWORD": "test-password",
			"DJANGO_SUPERUSER_PHONE": "1234567890",
		},
	)
	def test_creates_superuser_once(self):
		output = StringIO()

		call_command("ensure_superuser", stdout=output)
		call_command("ensure_superuser", stdout=output)

		user_model = get_user_model()
		user = user_model.objects.get(email="admin@example.com")
		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)
		self.assertTrue(user.check_password("test-password"))
		self.assertEqual(user_model.objects.count(), 1)
		self.assertIn("already exists", output.getvalue())

	@patch.dict(
		os.environ,
		{
			"DJANGO_SUPERUSER_EMAIL": "user@example.com",
			"DJANGO_SUPERUSER_PASSWORD": "test-password",
		},
	)
	def test_rejects_existing_non_superuser(self):
		user_model = get_user_model()
		user_model.objects.create_user(
			email="user@example.com",
			password="test-password",
		)

		with self.assertRaises(CommandError):
			call_command("ensure_superuser")
