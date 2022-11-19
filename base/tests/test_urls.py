from django.test import SimpleTestCase
from django.urls import reverse, resolve
from base.views import (
    RoomListView,
    RoomDetailView,
    RoomCreateView,
    RoomUpdateView,
    RoomDeleteView,
    MessageUpdateView,
    MessageDeleteView,
    TopicListView,
    MessageListView,
)


class TestUrls(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse("base:index")
        self.assertEqual(resolve(url).func.view_class, RoomListView)

    def test_room_detail_url_resolves(self):
        url = reverse("base:room_detail", args=["my-room"])
        self.assertEqual(resolve(url).func.view_class, RoomDetailView)

    def test_room_create_url_resolves(self):
        url = reverse("base:room_create")
        self.assertEqual(resolve(url).func.view_class, RoomCreateView)

    def test_room_update_url_resolves(self):
        url = reverse("base:room_update", args=["my-room"])
        self.assertEqual(resolve(url).func.view_class, RoomUpdateView)

    def test_room_delete_url_resolves(self):
        url = reverse("base:room_delete", args=["my-room"])
        self.assertEqual(resolve(url).func.view_class, RoomDeleteView)

    def test_message_update_url_resolves(self):
        url = reverse("base:message_update", args=[1])
        self.assertEqual(resolve(url).func.view_class, MessageUpdateView)

    def test_message_delete_url_resolves(self):
        url = reverse("base:message_delete", args=[1])
        self.assertEqual(resolve(url).func.view_class, MessageDeleteView)

    def test_topic_list_url_resolves(self):
        url = reverse("base:topic_list")
        self.assertEqual(resolve(url).func.view_class, TopicListView)

    def test_message_list_url_resolves(self):
        url = reverse("base:message_list")
        self.assertEqual(resolve(url).func.view_class, MessageListView)
