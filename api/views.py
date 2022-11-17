from django.db.models import Q
from django.contrib.auth import get_user_model

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from base.models import Room, Topic, Message
from .serializers import (
    RoomSerializer,
    UserSerializer,
    TopicSerializer,
    MessageSerializer,
)

from .paginations import CustomPagination


class APIRoot(APIView):
    def get(self, request, format=None):
        return Response(
            {
                "rooms": reverse("api:room_list", request=request, format=format),
                "users": reverse("api:user_list", request=request, format=format),
                "topics": reverse("api:topic_list", request=request, format=format),
                "messages": reverse("api:message_list", request=request, format=format),
            }
        )


class RoomList(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            try:
                return Room.objects.filter(
                    Q(topic__name__icontains=query) | Q(name__icontains=query)
                )
            except Room.DoesNotExist:
                pass
        else:
            return Room.objects.all()


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all().order_by("id")
    serializer_class = UserSerializer
    pagination_class = CustomPagination


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class TopicList(generics.ListAPIView):
    serializer_class = TopicSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            try:
                return Topic.objects.filter(name__icontains=query)
            except Topic.DoesNotExist:
                pass
        else:
            return Topic.objects.all()


class TopicDetail(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class MessageList(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = CustomPagination


class MessageDetail(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
