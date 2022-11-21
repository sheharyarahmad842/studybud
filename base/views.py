from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.urls import reverse_lazy
from .models import Room, Topic, Message
from .forms import RoomForm, MessageForm


class RoomListView(ListView):
    model = Room
    template_name = "base/index.html"
    context_object_name = "room_list"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            return Room.objects.annotate(
                search=SearchVector("topic__name", "host__username"),
            ).filter(search=query)
        else:
            return Room.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_list"] = Topic.objects.all()[0:5]
        context["room_messages"] = Message.objects.all()
        return context


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
    template_name = "base/room_update.html"

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
        if query:
            queryset = Topic.objects.filter(name__icontains=query)
        else:
            queryset = Topic.objects.all()
        return queryset


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "base/message_list.html"
    context_object_name = "room_messages"
