from django.urls import path

from habit import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('habit/<habit_pk>/', views.HabitView.as_view(), name='habit'),
    path('day/<day_pk>/', views.DayView.as_view(), name='day')
]
