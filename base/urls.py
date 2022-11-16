from django.urls import path
from .views import (
    # HomePageView,
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

app_name = "base"

urlpatterns = [
    path("", RoomListView.as_view(), name="index"),
    path("rooms/<slug:slug>/", RoomDetailView.as_view(), name="room_detail"),
    path("create_room/", RoomCreateView.as_view(), name="create_room"),
    path("<slug:slug>/update/", RoomUpdateView.as_view(), name="room_update"),
    path("<slug:slug>/delete/", RoomDeleteView.as_view(), name="room_delete"),
    path(
        "message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("topics/", TopicListView.as_view(), name="topic_list"),
    path("messages/", MessageListView.as_view(), name="message_list"),
]
