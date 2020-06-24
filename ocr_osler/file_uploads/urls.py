from django.urls import path
from . import views
from django.conf.urls import url


app_name = "file_uploads"
urlpatterns = [
    path(
        route='',
        view=views.File_uploadListView.as_view(),
        name='list'
    ),
    path(
        route='add/',
        view=views.File_uploadCreateView.as_view(),
        name='add'
    ),
    path(
        route='<slug:slug>/',
        view=views.File_uploadDetailView.as_view(),
        name='detail'
    ),
    path(
        route='<slug:slug>/update/',
        view=views.File_uploadUpdateView.as_view(),
        name='update'
    ),
]
