from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from base.models import Topic, Room, Message
from base.views import RoomDetailView


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.host = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="9a8b7c6d"
        )
        cls.topic = Topic.objects.create(name="python")
        cls.room = Room.objects.create(
            host=cls.host,
            topic=cls.topic,
            name="Master Python",
            description="It is a python room",
        )
        cls.user = get_user_model().objects.create_user(
            username="testuser123", email="testuser123@email.com", password="9a8b7c6d"
        )
        cls.message1 = Message.objects.create(
            user=cls.user, room=cls.room, body="Message 1"
        )
        cls.message2 = Message.objects.create(
            user=cls.user, room=cls.room, body="Message 2"
        )

    def test_str_func_of_topic_model_returns_correct_name(self):
        self.assertEqual(str(self.topic), self.topic.name)

    def test_str_func_of_room_model_returns_correct_name(self):
        self.assertEqual(str(self.room), self.room.name)

    def test_room_is_assigned_slug_on_creation(self):
        self.assertEqual(self.room.slug, "master-python")

    def test_room_participants_count_must_be_zero(self):
        self.assertEqual(self.room.participants.count(), 0)

    def test_room_participants_count_must_be_one(self):
        participant = get_user_model().objects.create_user(
            username="participant", email="participant@email.com", password="9a8b7c6d"
        )
        self.room.participants.add(participant)
        self.assertEqual(self.room.participants.count(), 1)

    def test_get_absolute_url_method_of_room(self):
        url = reverse("base:room_detail", args=[self.room.slug])
        self.assertEqual(resolve(url).func.view_class, RoomDetailView)

    def test_count_total_messages_that_exist_in_room(self):
        self.assertEqual(self.room.messages.count(), 2)

    def test_count_total_messages_written_by_user(self):
        self.assertEqual(self.user.messages.count(), 2)

    def test_str_func_of_message_model_returns_correct_name(self):
        self.assertEqual(str(self.message1), self.message1.body[:50])
