from django.urls import path

from ..views.my_info import MyInfoView

urlpatterns = [
    path("", MyInfoView.as_view(), name="my-info"),
]
