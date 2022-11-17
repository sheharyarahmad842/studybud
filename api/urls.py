from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import (
    APIRoot,
    RoomList,
    RoomDetail,
    UserList,
    UserDetail,
    TopicList,
    TopicDetail,
    MessageList,
    MessageDetail,
)

app_name = "api"

urlpatterns = [
    path("", APIRoot.as_view(), name="api_root"),
    path("rooms/", RoomList.as_view(), name="room_list"),
    path("rooms/<int:pk>/", RoomDetail.as_view(), name="room_detail"),
    path("users/", UserList.as_view(), name="user_list"),
    path("user/<int:pk>/", UserDetail.as_view(), name="user_detail"),
    path("topics/", TopicList.as_view(), name="topic_list"),
    path("topic/<int:pk>/", TopicDetail.as_view(), name="topic_detail"),
    path("messages/", MessageList.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetail.as_view(), name="message_detail"),
]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=["json", "html"])
