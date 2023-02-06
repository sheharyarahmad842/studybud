from django.contrib.auth import get_user_model
from rest_framework import serializers
from base.models import Room, Topic, Message


class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()
    messages = serializers.HyperlinkedRelatedField(
        many=True, view_name="api:message_detail", read_only=True
    )
    host = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Room
        fields = [
            "id",
            "host",
            "topic",
            "name",
            "participants",
            "total_messages",
            "messages",
            "description",
            "created_on",
        ]

    def to_representation(self, instance):
        rep = super(RoomSerializer, self).to_representation(instance)
        rep["host"] = instance.host.username
        rep["topic"] = instance.topic.name
        return rep

    def get_total_messages(self, room):
        return room.messages.count()


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     rooms = serializers.HyperlinkedRelatedField(
#         many=True,
#         view_name="api:room_detail",
#         read_only=True,
#     )
#     topics = serializers.HyperlinkedRelatedField(
#         many=True,
#         view_name="api:topic_detail",
#         read_only=True,
#     )
#     messages = serializers.HyperlinkedRelatedField(
#         many=True, view_name="api:message_detail", read_only=True
#     )

#     class Meta:
#         model = get_user_model()
#         fields = [
#             "id",
#             "username",
#             "email",
#             "rooms",
#             "messages",
#         ]


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    total_rooms = serializers.SerializerMethodField()
    rooms = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="api:room_detail"
    )
    host = serializers.PrimaryKeyRelatedField(
        source="host.username", read_only=True, many=False
    )
    # Hide the host field in form and set to default user
    host = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Topic
        fields = ["id", "name", "total_rooms", "rooms", "host"]

    def get_total_rooms(self, topic):
        return topic.rooms.count()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "user", "room", "body", "created_on"]

    def to_representation(self, instance):
        rep = super(MessageSerializer, self).to_representation(instance)
        rep["user"] = instance.user.username
        rep["room"] = instance.room.name
        return rep
