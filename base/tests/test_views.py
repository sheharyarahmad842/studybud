from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from base.models import Topic, Room


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.host = get_user_model().objects.create_user(
            username="shery", email="shery@email.com", password="9a8b7c6d"
        )
        cls.topic = Topic.objects.create(host=cls.host, name="Test")
        cls.room = Room.objects.create(
            host=cls.host,
            topic=cls.topic,
            name="Test room",
        )
        cls.test_room = Room.objects.create(
            host=cls.host, topic=cls.topic, name="Room for deleting"
        )
        cls.test_user = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="9a8b7c6d"
        )

    def setUp(self):
        self.client = Client()
        self.index_url = reverse("base:index")
        self.detail_url = reverse("base:room_detail", args=[self.room.slug])
        self.create_room_url = reverse("base:room_create")
        self.delete_room_url = reverse("base:room_delete", args=[self.test_room.slug])
        self.topic_list_url = reverse("base:topic_list")
        self.message_list_url = reverse("base:message_list")

    def test_room_list_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base/index.html")

    def test_room_detail_GET(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base/room_detail.html")

    def test_room_detail_POST_adds_new_comment(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.post(
            self.detail_url,
            {"user": self.test_user, "room": self.room, "body": "Test Comment"},
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.room.messages.first().body, "Test Comment")
        self.assertEquals(self.room.messages.count(), 1)

    def test_room_create_GET_shows_room_form(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.create_room_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base/room_form.html")

    def test_room_create_POST_creates_new_room(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.post(
            self.create_room_url,
            {
                "host": self.host,
                "topic": self.topic,
                "name": "Test Room 2",
                "description": "Room for testing purposes",
            },
        )
        room2 = Room.objects.get(slug="test-room-2")
        self.assertEquals(response.status_code, 302)
        self.assertEquals(room2.name, "Test Room 2")

    def test_room_update_GET_shows_room_form(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        test_room = Room.objects.create(
            host=self.host, topic=self.topic, name="Testing"
        )
        response = self.client.get(reverse("base:room_update", args=[test_room.slug]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base/room_form.html")

    def test_room_update_POST_updates_existing_room(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        test_room = Room.objects.create(
            host=self.host, topic=self.topic, name="Testing"
        )
        response = self.client.post(
            reverse("base:room_update", args=[test_room.slug]),
            {
                "host": self.host,
                "topic": self.topic,
                "name": "My Test Room",
            },
        )
        self.assertEquals(response.status_code, 302)
        self.assertEquals(test_room.name, "My Test Room")
        self.assertEqual(test_room.host, self.host)
        self.assertEqual(test_room.topic, self.topic)

    def test_room_delete_POST_deletes_a_room(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.delete(self.delete_room_url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(self.host.rooms.count(), 1)

    def test_topic_list_GET(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.topic_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base/topic_list.html")

    def test_message_list_GET(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.message_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "base/message_list.html")
