from django.urls import path

from .views import ScheduleView, UserCreate, StartupInfo

urlpatterns = [
    path('schedule', ScheduleView.as_view(), name='get-schedule'),
    path('user', UserCreate.as_view()),
    path('startup_info', StartupInfo.as_view())
]
