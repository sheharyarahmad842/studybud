from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = "base/topic_list.html"
    context_object_name = "topic_list"

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            queryset = (
                Topic.objects.annotate(total_rooms=Count("rooms"))
                .filter(total_rooms__gt=0, name__icontains=query)
                .order_by("-total_rooms", "-added_on")
            )
        else:
            queryset = (
                Topic.objects.annotate(total_rooms=Count("rooms"))
                .filter(total_rooms__gt=0)
                .order_by("-total_rooms", "-added_on")
            )
        return queryset


class RoomListView(ListView):
    model = Room
    template_name = "base/index.html"
    context_object_name = "room_list"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            return Room.objects.filter(
                Q(topic__name=query) | Q(host__username=query) | Q(name=query)
            )
        else:
            return Room.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_list"] = (
            Topic.objects.annotate(total_rooms=Count("rooms"))
            .filter(total_rooms__gt=0)
            .order_by("-total_rooms", "-added_on")[:5]
        )
        context["room_messages"] = Message.objects.all()
        context["total_topics"] = Topic.objects.annotate(
            total_rooms=Count("rooms")
        ).filter(total_rooms__gt=0)
        return context


class RoomDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        room = get_object_or_404(Room, slug=self.kwargs["slug"])
        room_messages = Message.objects.filter(room=room)
        participants = room.participants.all()
        form = MessageForm()
        context = {
            "room": room,
            "form": form,
            "room_messages": room_messages,
            "participants": participants,
        }
        return render(request, "base/room_detail.html", context)

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, slug=self.kwargs["slug"])
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        message.save()
        messages.success(request, "Your message was added successfully.")
        room.participants.add(request.user.profile)
        return redirect(room.get_absolute_url())


class RoomCreateView(LoginRequiredMixin, CreateView):
    form_class = RoomForm
    template_name = "base/room_form.html"

    def post(self, request, *args, **kwargs):
        super(RoomCreateView, self).post(request, *args, **kwargs)
        topic_name = request.POST.get("topic").capitalize()
        topic = Topic.objects.get_or_create(name=topic_name)[0]
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
        context["form"] = RoomForm(
            data={
                "topic": self.object.topic.name,
                "name": self.object.name,
                "description": self.object.description,
            }
        )
        context["update"] = True
        return context

    def post(self, request, *args, **kwargs):
        super(RoomUpdateView, self).post(request, *args, **kwargs)
        room = self.object
        topic_name = request.POST.get("topic").capitalize()
        topic = Topic.objects.get_or_create(name=topic_name)[0]
        room.name = request.POST.get("name")
        room.topic = topic
        room.slug = slugify(room.name)
        room.description = request.POST.get("description")
        room.save()
        return redirect(self.object.get_absolute_url())


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = "base/room_delete.html"
    context_object_name = "room"
    success_url = reverse_lazy("base:index")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "base/message_list.html"
    context_object_name = "room_messages"


class MessageUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        message = Message.objects.get(pk=self.kwargs["pk"])
        room_messages = Message.objects.filter(room=message.room)
        form = MessageForm(instance=message)
        context = {
            "form": form,
            "room": message.room,
            "participants": message.room.participants.all,
            "room_messages": room_messages,
        }
        return render(request, "base/room_detail.html", context)

    def post(self, request, *args, **kwargs):
        message = Message.objects.get(pk=self.kwargs["pk"])
        message.body = request.POST.get("body")
        message.save()
        messages.success(request, "Your message was updated successfully.")
        return redirect(message.room.get_absolute_url())


def message_delete_view(request, pk):
    message = Message.objects.get(id=pk)
    room = message.room
    if request.method == "POST":
        message.delete()
        messages.error(request, "Your message was deleted successfully.")
        return redirect("base:room_detail", slug=room.slug)
    total_messages = Message.objects.filter(
        user=request.user, room=message.room
    ).count()
    if total_messages == 1:
        room.participants.remove(request.user.profile)
    return render(request, "base/message_delete.html")
