from django.urls import path
from .views import MyTaskListView, TaskCreateView, TaskCompleteView,index, LinkTelegramView
from .views import TelegramTaskList, TelegramCompleteTask
urlpatterns = [
  
    path('my-tasks/', MyTaskListView.as_view(), name='my-tasks'),
    path('create-task/', TaskCreateView.as_view(), name='create-task'),
    path('complete-task/<int:pk>/', TaskCompleteView.as_view(), name='complete-task'),
    path('link-telegram/', LinkTelegramView.as_view(), name='link-telegram'),
    path('telegram/tasks/', TelegramTaskList.as_view(), name='telegram-tasks'),
    path('telegram/complete-task/', TelegramCompleteTask.as_view(), name='telegram-complete-task'),
    path('', index)
]