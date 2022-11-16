from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm


class RoomListView(ListView):
    model = Room
    template_name = "base/index.html"
    context_object_name = "room_list"

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query == None:
            queryset = Room.objects.all()
        else:
            queryset = Room.objects.filter(
                Q(topic__name__icontains=query) | Q(host__username__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_list"] = Topic.objects.all()[0:5]
        context["room_messages"] = Message.objects.all()
        return context


# @login_required(login_url="account_login")
# def room_detail_view(request, slug):
#     room = get_object_or_404(Room, slug=slug)
#     messages = Message.objects.filter(room=room)
#     participants = room.participants.all()
#     form = MessageForm()

#     if request.method == "POST":
#         message = Message.objects.create(
#             user=request.user, room=room, body=request.POST.get("body")
#         )
#         room.participants.add(request.user)

#     context = {
#         "room": room,
#         "form": form,
#         "messages": messages,
#         "participants": participants,
#     }
#     return render(request, "base/room_detail.html", context)


class RoomDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, slug=self.kwargs["slug"])
        messages = Message.objects.filter(room=room)
        participants = room.participants.all()
        form = MessageForm()
        context = {
            "room": room,
            "form": form,
            "messages": messages,
            "participants": participants,
        }
        return render(request, "base/room_detail.html", context)

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, slug=self.kwargs["slug"])
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        message.save()
        room.participants.add(request.user)
        return redirect(room.get_absolute_url())


class RoomCreateView(LoginRequiredMixin, CreateView):
    form_class = RoomForm
    template_name = "base/room_form.html"
    success_url = reverse_lazy("base:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_list"] = Topic.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        super(RoomCreateView, self).post(request, *args, **kwargs)
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        name = request.POST.get("name")
        description = request.POST.get("description")
        Room.objects.create(
            host=request.user, topic=topic, name=name, description=description
        )
        return redirect("base:index")


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    fields = ("topic", "name", "description")
    template_name = "base/room_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room"] = self.object
        context["update"] = True
        return context

    def post(self, request, *args, **kwargs):
        super(RoomUpdateView, self).post(request, *args, **kwargs)
        room = self.object
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect(self.object.get_absolute_url())


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = "base/room_delete.html"
    context_object_name = "room"
    success_url = reverse_lazy("base:index")


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ("body",)
    template_name = "base/message_update.html"

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("base:room_detail", kwargs={"slug": self.object.room.slug})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "base/message_delete.html"
    context_object_name = "message"

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("base:room_detail", kwargs={"slug": self.object.room.slug})


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = "base/topic_list.html"
    context_object_name = "topic_list"

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query == None:
            queryset = Topic.objects.all()
        else:
            queryset = Topic.objects.filter(name__icontains=query)
        return queryset


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "base/message_list.html"
    context_object_name = "room_messages"
