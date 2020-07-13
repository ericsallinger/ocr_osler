from . models import File_upload
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from . serializers import File_uploadSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class File_uploadCreateAPIView(ListCreateAPIView):
    queryset = File_upload.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = File_uploadSerializer
    lookup_field = 'uuid'


class File_uploadRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = File_upload.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = File_uploadSerializer
    lookup_field = 'uuid'
