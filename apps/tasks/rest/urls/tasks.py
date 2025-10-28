from django.urls import path

from ..views.tasks import MyTaskListCreateView

urlpatterns = [
    path("", MyTaskListCreateView.as_view(), name="my-task-list-create"),
]
