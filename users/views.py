from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from base.models import Topic
from users.models import Profile
from .forms import ProfileForm

# Create your views here.
@login_required(login_url="account_login")
def user_profile(request, pk):
    user = Profile.objects.get(pk=pk)
    topic_list = (
        Topic.objects.annotate(total_rooms=Count("rooms"))
        .filter(total_rooms__gt=0)
        .order_by("-total_rooms", "-added_on")[:5]
    )
    room_list = user.rooms.all()
    room_messages = user.messages.all()
    total_topics = Topic.objects.annotate(total_rooms=Count("rooms")).filter(
        total_rooms__gt=0
    )
    context = {
        "user": user,
        "room_list": room_list,
        "room_messages": room_messages,
        "topic_list": topic_list,
        "total_topics": total_topics,
    }
    return render(request, "users/profile.html", context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "users/update_profile.html"

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("users:profile", kwargs={"pk": self.object.pk})
