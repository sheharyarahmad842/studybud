from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from base.models import Topic, Room, Message


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.host = get_user_model().objects.create_user(
            username="shery", email="shery@email.com", password="9a8b7c6d"
        )
        cls.topic = Topic.objects.create(name="Test")
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
        cls.message = Message.objects.create(
            room=cls.room, user=cls.test_user, body="Test Message"
        )
        cls.test_message = Message.objects.create(
            room=cls.room, user=cls.test_user, body="Delete Message"
        )

    def setUp(self):
        self.client = Client()
        self.index_url = reverse("base:index")
        self.detail_url = reverse("base:room_detail", args=[self.room.slug])
        self.create_room_url = reverse("base:room_create")
        self.delete_room_url = reverse("base:room_delete", args=[self.test_room.slug])
        self.topic_list_url = reverse("base:topic_list")
        self.message_list_url = reverse("base:message_list")
        self.message_update_url = reverse("base:message_update", args=[self.message.id])
        self.message_delete_url = reverse(
            "base:message_delete", args=[self.test_message.id]
        )

    def test_room_list_GET(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/index.html")

    def test_room_detail_GET(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/room_detail.html")

    def test_room_detail_POST_adds_new_message(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.post(
            self.detail_url,
            {"user": self.test_user, "room": self.room, "body": "Test Comment"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.room.messages.first().body, "Test Comment")
        self.assertEqual(self.room.messages.count(), 3)

    def test_room_POST_updates_existing_message(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.post(
            self.message_update_url,
            {"user": self.test_user, "room": self.room, "body": "Comment Updated"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.room.messages.first().body, "Comment Updated")
        self.assertEqual(self.room.messages.count(), 2)

    def test_message_list_GET(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.message_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/message_list.html")

    def test_message_delete_GET_shows_confirmation_page(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.message_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete this comment?")
        self.assertTemplateUsed(response, "base/message_delete.html")

    def test_message_delete_POST_redirects_and_deletes_a_message(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        self.assertEqual(self.room.messages.count(), 2)
        self.client.post(self.message_delete_url)
        self.room.refresh_from_db()
        self.assertEqual(self.room.messages.count(), 1)

    def test_room_create_GET_shows_room_form(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.create_room_url)
        self.assertEqual(response.status_code, 200)
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
        self.assertEqual(response.status_code, 302)
        self.assertEqual(room2.name, "Test Room 2")

    def test_room_update_GET_shows_room_form(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        test_room = Room.objects.create(
            host=self.host, topic=self.topic, name="Testing"
        )
        response = self.client.get(reverse("base:room_update", args=[test_room.slug]))

        self.assertEqual(response.status_code, 200)
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
        self.assertEqual(response.status_code, 302)
        test_room.refresh_from_db()
        self.assertEqual(test_room.name, "My Test Room")
        self.assertEqual(test_room.host, self.host)
        self.assertEqual(test_room.topic, self.topic)

    def test_room_delete_GET_shows_confirmation_page(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.delete_room_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, f'Are you sure you want to delete "{self.test_room.name}"?'
        )
        self.assertTemplateUsed(response, "base/room_delete.html")

    def test_room_delete_POST_deletes_a_room(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.delete(self.delete_room_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.host.rooms.count(), 1)

    def test_topic_list_GET(self):
        self.client.login(email="testuser@email.com", password="9a8b7c6d")
        response = self.client.get(self.topic_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base/topic_list.html")
