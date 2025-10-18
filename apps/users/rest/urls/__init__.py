from django.urls import path, include

urlpatterns = [
    path("my-info/", include("apps.users.rest.urls.my_info")),
]
