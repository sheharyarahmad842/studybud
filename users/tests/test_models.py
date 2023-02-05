from django.test import TestCase
import tempfile
from django.contrib.auth import get_user_model


User = get_user_model()


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="9a8b7c6d",
            name="Test User",
            avatar=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        )

    def test_create_user_fields(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@email.com")
        self.assertEqual(self.user.name, "Test User")

    def test_create_user_avatar(self):
        self.assertTrue(self.user.avatar.url)
