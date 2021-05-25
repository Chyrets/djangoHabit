from django.urls import path

from habit import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
]
