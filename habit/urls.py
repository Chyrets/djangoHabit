from django.urls import path

from habit import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
    path('habits/', views.AllHabitView.as_view(), name='list_of_habits'),
    path('habit/<habit_pk>/', views.HabitView.as_view(), name='habit'),
    path('day/<day_pk>/', views.DayView.as_view(), name='day'),
    path('create-habit/', views.CreateHabitView.as_view(), name='create_habit'),
]
