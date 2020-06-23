from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import File_upload



class File_uploadListView(ListView):
    model = File_upload


class File_uploadDetailView(DetailView):
    model = File_upload


class File_uploadCreateView(LoginRequiredMixin, CreateView):
    model = File_upload
    fields = [
        'name',
        'description',
        'firmness',
        'country_of_origin',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class File_uploadUpdateView(LoginRequiredMixin, UpdateView):
    model = File_upload
    fields = [
        'name',
    ]
    action = "Update"


