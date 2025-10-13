from django.urls import path
from .views import MyTaskListView, TaskCreateView, TaskCompleteView

urlpatterns = [
    path('my-tasks/', MyTaskListView.as_view(), name='my-tasks'),
    path('create-task/', TaskCreateView.as_view(), name='create-task'),
    path('complete-task/<int:pk>/', TaskCompleteView.as_view(), name='complete-task'),
]