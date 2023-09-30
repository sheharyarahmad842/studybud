from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions

# from rest_framework.response import Response
# from rest_framework.reverse import reverse
# from rest_framework.views import APIView

from base.models import Room, Topic, Message
from .serializers import (
    RoomSerializer,
    TopicSerializer,
    MessageSerializer,
)

from .paginations import CustomPagination
from .permissions import IsHostOrReadOnly, IsMessageUserOrReadOnly


# class APIRoot(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, format=None):
#         return Response(
#             {
#                 "rooms": reverse("api:room_list", request=request, format=format),
#                 # "users": reverse("api:user_list", request=request, format=format),
#                 "topics": reverse("api:topic_list", request=request, format=format),
#                 "messages": reverse("api:message_list", request=request, format=format),
#             }
#         )


class RoomList(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            try:
                return Room.objects.filter(Q(topic__name=query) | Q(name=query))
            except Room.DoesNotExist:
                pass
        else:
            return Room.objects.all()


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsHostOrReadOnly]


# class UserList(generics.ListAPIView):
#     queryset = get_user_model().objects.all().order_by("id")
#     serializer_class = UserSerializer
#     pagination_class = CustomPagination
#     permission_classes = [permissions.IsAuthenticated]


# class UserDetail(generics.RetrieveAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAdminUser]


class TopicList(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            try:
                return Topic.objects.filter(name__icontains=query)
            except Topic.DoesNotExist:
                pass
        else:
            return Topic.objects.all()


class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsHostOrReadOnly]


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsMessageUserOrReadOnly]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["name"] = user.first_name
        token["email"] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
