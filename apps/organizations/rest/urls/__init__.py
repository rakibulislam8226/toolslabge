from django.urls import path, include

urlpatterns = [
    path("register/", include("apps.organizations.rest.urls.register")),
]
