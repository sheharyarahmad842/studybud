from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from base.models import Topic
from users.models import Profile
from .forms import ProfileForm

# Create your views here.
@login_required(login_url="account_login")
def user_profile(request, pk):
    user_profile = Profile.objects.get(id=pk)
    topic_list = (
        Topic.objects.annotate(total_rooms=Count("rooms"))
        .filter(total_rooms__gt=0)
        .order_by("-total_rooms", "-added_on")[:5]
    )
    room_list = user_profile.user.rooms.all()
    room_messages = user_profile.user.messages.all()
    total_topics = Topic.objects.annotate(total_rooms=Count("rooms")).filter(
        total_rooms__gt=0
    )
    context = {
        "user_profile": user_profile,
        "room_list": room_list,
        "room_messages": room_messages,
        "topic_list": topic_list,
        "total_topics": total_topics,
    }
    return render(request, "users/profile.html", context)


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(id=kwargs.get("pk"))
        form = ProfileForm(
            instance=user_profile,
            initial={"name": request.user.name, "username": request.user.username},
        )
        context = {"user_profile": user_profile, "form": form}
        return render(request, "users/update_profile.html", context)

    def post(self, request, *args, **kwargs):
        user_profile = Profile.objects.get(id=kwargs.get("pk"))
        form = ProfileForm(
            instance=user_profile, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            name = form.cleaned_data["name"]
            username = form.cleaned_data["username"]
            avatar = form.cleaned_data["avatar"]
            bio = form.cleaned_data["bio"]
            request.user.name = name
            try:
                request.user.username = username
                request.user.save()
            except:
                messages.error(
                    request, f"User with the username {username} already exists."
                )
                return redirect("users:update_profile", pk=user_profile.pk)
            user_profile.avatar = avatar
            user_profile.bio = bio
            user_profile.save()
            messages.success(request, "Your Profile was updated successfully.")
            return redirect(user_profile.get_absolute_url())
        else:
            messages.error(
                request, "There was a problem updating your profile. Please try again"
            )
            return redirect(user_profile.get_absolute_url())
