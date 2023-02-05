from django.test import TestCase
from base.forms import RoomForm, MessageForm
from base.models import Topic


class TestForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.topic = Topic.objects.create(name="Python")

    def test_room_form_is_valid(self):

        form = RoomForm(
            data={
                "topic": self.topic,
                "name": "Master python",
                "description": "It is a room for python developers",
            }
        )

        self.assertTrue(form.is_valid())

    def test_room_form_no_data(self):
        form = RoomForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_message_form_is_valid(self):
        form = MessageForm(
            data={
                "body": "It is a test comment",
            }
        )

        self.assertTrue(form.is_valid())

    def test_message_form_no_data(self):
        form = MessageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
