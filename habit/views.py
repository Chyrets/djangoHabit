from datetime import datetime

from django.shortcuts import render
from django.views import View

from habit.models import Day, Habit


class MainPage(View):
    """
    This page display tasks for today
    """

    def get(self, request, *args, **kwargs):
        tasks = Habit.objects.filter(day__date=datetime.today(), user=request.user)

        context = {
            'tasks': tasks
        }

        return render(request, 'habit/main.html', context)
