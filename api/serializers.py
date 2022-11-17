from django.contrib.auth import get_user_model
from rest_framework import serializers
from base.models import Room, Topic, Message


class RoomSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()
    messages = serializers.HyperlinkedRelatedField(
        many=True, view_name="api:message_detail", read_only=True
    )

    class Meta:
        model = Room
        fields = [
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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    rooms = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="api:room_detail",
        read_only=True,
    )
    messages = serializers.HyperlinkedRelatedField(
        many=True, view_name="api:message_detail", read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "bio", "rooms", "messages", "avatar"]


class TopicSerializer(serializers.HyperlinkedModelSerializer):
    total_rooms = serializers.SerializerMethodField()
    rooms = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="api:room_detail"
    )

    class Meta:
        model = Topic
        fields = ["name", "total_rooms", "rooms"]

    def get_total_rooms(self, topic):
        return topic.rooms.count()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["user", "room", "body", "created_on"]

    def to_representation(self, instance):
        rep = super(MessageSerializer, self).to_representation(instance)
        rep["user"] = instance.user.username
        rep["room"] = instance.room.name
        return rep
