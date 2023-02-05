from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import ProfileUpdateView, user_profile


class TestUrls(SimpleTestCase):
    def test_user_profile_url_resolves(self):
        url = reverse("users:profile", args=[1])
        self.assertEqual(resolve(url).func, user_profile)

    def test_user_update_profile_url_resolves(self):
        url = reverse("users:update_profile", args=[1])
        self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)
