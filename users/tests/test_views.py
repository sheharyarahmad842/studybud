from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from base.models import Topic, Room, Message


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@email.com",
            password="9a8b7c6d",
            avatar=r"./media/avatar.svg",
        )

    def setUp(self):
        self.client = Client()
        self.user_profile_url = reverse("users:profile", args=[self.test_user.id])
        self.user_profile_update_url = reverse(
            "users:profile", args=[self.test_user.id]
        )

    def test_user_profile_GET_shows_user_profile_data(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_user_profile_update_GET_shows_form_with_user_data(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.user_profile_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/update_profile.html")

    def test_user_profile_update_POST_updates_existing_user_data(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")

        response = self.client.post(
            reverse("users:profile", args=[self.test_user.id]),
            {
                "avatar": r"./media/profile_pics/default.jpg",
                "username": self.test_user.username,
                "email": self.test_user.email,
                "bio": "I am a test user",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, "testuser")
        self.assertEqual(self.test_user.email, "testuser@email.com")
        self.assertEqual(self.test_user.bio, "I am a test user")
        self.assertContains(self.test_user.avatar.url, "default")
