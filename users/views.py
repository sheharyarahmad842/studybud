from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from base.models import Topic
from .forms import ProfileForm

# Create your views here.
@login_required(login_url='account_login')
def user_profile(request, pk):
    user = get_user_model().objects.get(pk=pk)
    topic_list = Topic.objects.all()
    room_list = user.rooms.all()
    room_messages = user.messages.all()
    context = {
        'user': user, 
        'room_list': room_list, 
        'room_messages': room_messages,
        'topic_list': topic_list
    }
    return render(request, 'users/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileForm
    template_name = 'users/update_profile.html'
    login_url = 'account_login'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})


