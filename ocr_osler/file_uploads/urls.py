from django.urls import path
from . import views
from django.conf.urls import url


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
app_name = "file_uploads"
urlpatterns = [
    # REST API
    # /file_uploads/api/
    url(
        regex=r'^api/$',
        view=views.File_uploadCreateAPIView.as_view(),
        name='file_rest_api'
    ),
    # /file_uploads/api/:slug/
    url(
        regex=r'^api/(?P<uuid>[-\w]+)/$',
        view=views.File_uploadRetrieveUpdateDestroyAPIView.as_view(),
        name='file_rest_api'
    ),
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
