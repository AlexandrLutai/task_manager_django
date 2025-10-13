from django.urls import path
from .views import MyTaskListView, TaskCreateView, TaskCompleteView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('my-tasks/', MyTaskListView.as_view(), name='my-tasks'),
    path('create-task/', TaskCreateView.as_view(), name='create-task'),
    path('complete-task/<int:pk>/', TaskCompleteView.as_view(), name='complete-task'),

    # JWT:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]